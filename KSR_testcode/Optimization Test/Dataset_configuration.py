import os
import cv2
import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from torchvision import transforms
import albumentations as A 
from facenet_pytorch import MTCNN
import pandas as pd
from collections import Counter

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# 얼굴 인식 및 전처리 클래스
class MTCNNPreprocess:
    def __init__(self):
        self.detector = MTCNN(keep_all=False, device='cuda' if torch.cuda.is_available() else 'cpu')

    def __call__(self, frame):
        faces = self.detector.detect(frame)[0]
        if faces is None or len(faces) == 0:
            return None  # 얼굴 검출 실패

        faces_list = []
        for face in faces:
            x1, y1, x2, y2 = map(int, face)
            h, w, _ = frame.shape
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)  # 이미지 크기 초과 방지
            face_region = frame[y1:y2, x1:x2]

            if face_region.size == 0:  # face가 비어있으면 None 반환
                continue

            faces_list.append(face_region)

        return faces_list

# 데이터 증강 클래스
class DataAugmentation:
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
        self.transform = A.Compose([
            A.HorizontalFlip(p=0.5),  # 랜덤 수평 뒤집기
            A.VerticalFlip(p=0.2),   # 랜덤 수직 뒤집기
            A.RandomBrightnessContrast(p=0.5),  # 밝기 및 대비 조정
            A.Rotate(limit=45, p=0.5),  # 랜덤 회전 (최대 45도)
            A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.5),  # 이동, 스케일, 회전
            A.RandomGamma(p=0.2),  # 감마 변환
            A.GaussNoise(p=0.3),   # 가우시안 노이즈 추가
            A.MotionBlur(blur_limit=5, p=0.3),  # 모션 블러 추가
            A.ColorJitter(p=0.2),  # 색상 변화
            A.CLAHE(clip_limit=2.0, p=0.3),  # 히스토그램 평활화
            A.ElasticTransform(alpha=120, sigma=120 * 0.05, p=0.2),  # 탄성 변형, alpha_affine 제거
            A.Blur(blur_limit=3, p=0.1),  # 블러
            A.Sharpen(alpha=(0.2, 0.5), lightness=(0.5, 1.0), p=0.3),  # 선명화
            A.RandomResizedCrop(height=224, width=224, scale=(0.8, 1.0), ratio=(0.75, 1.33), p=0.3),  # 랜덤 크롭 후 리사이즈
            A.CoarseDropout(max_holes=8, max_height=16, max_width=16, min_holes=1, min_height=4, min_width=4, 
                            fill_value=0, p=0.5)  # 랜덤 마스킹
        ])

    def __call__(self, frame):
        augmented = self.transform(image=frame)["image"]
        resized = cv2.resize(augmented, self.target_size)
        return resized

# 비디오 데이터셋 클래스
class VideoFrameDataset(Dataset):
    def __init__(self, video_dir, df, preprocess, albumentations_transform=None, num_frames=10, target_size=(224, 224), augment=False):
        self.video_dir = video_dir
        self.df = df
        self.preprocess = preprocess
        self.albumentations_transform = albumentations_transform if augment else None
        self.num_frames = num_frames
        self.target_size = target_size
        self.frames_and_labels = self._load_frames_and_labels()

    def _load_frames_and_labels(self):
        frames_and_labels = []
        for _, row in self.df.iterrows():
            video_file = row['video_name']
            label = row.get('label', -1)  # 테스트 데이터는 라벨 없이 처리

            video_path = os.path.join(self.video_dir, video_file)
            if not os.path.exists(video_path):
                print(f"Warning: {video_file} does not exist. Skipping.")
                continue

            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_interval = max(total_frames // self.num_frames, 1)
            valid_frames = []

            for i in range(self.num_frames):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval)
                success, frame = cap.read()
                if not success:
                    continue

                faces = self.preprocess(frame)
                if faces is None:
                    continue

                for face in faces:
                    if self.albumentations_transform is not None:
                        face = self.albumentations_transform(face)

                    face_resized = cv2.resize(face, self.target_size)
                    valid_frames.append((face_resized, label))

            cap.release()

            if valid_frames:
                frames_and_labels.extend(valid_frames)

        return frames_and_labels

    def __len__(self):
        return len(self.frames_and_labels)

    def __getitem__(self, idx):
        frame, label = self.frames_and_labels[idx]
        frame_tensor = transforms.ToTensor()(frame)
        return frame_tensor, label

# 오버샘플링을 위한 샘플링 가중치 생성 함수
def create_balanced_sampler(dataset):
    labels = [label for _, label in dataset.frames_and_labels]  # 모든 레이블 추출
    label_counts = Counter(labels)  # 레이블별 개수

    # 각 클래스의 목표 샘플 수를 최대 클래스 수로 맞춤
    max_count = max(label_counts.values())  # 가장 많은 클래스 샘플 수

    # 클래스별 가중치 계산 (1:1 비율로 샘플링)
    class_weights = {label: max_count / count for label, count in label_counts.items()}
    sample_weights = [class_weights[label] for label in labels]

    # WeightedRandomSampler 생성
    sampler = WeightedRandomSampler(sample_weights, num_samples=max_count * len(label_counts), replacement=True)
    return sampler



# CSV 파일 로드
train_data = pd.read_csv('/kaggle/working/train_data.csv')
test_data = pd.read_csv('/kaggle/working/test_data.csv')

# 데이터셋 및 로더 생성
preprocess = MTCNNPreprocess()
albumentations_transform = DataAugmentation()

# 훈련 데이터셋 (모든 데이터 증강 포함)
train_dataset = VideoFrameDataset(
    video_dir='/kaggle/input/traindataset0',  # 콤마 추가
    df=train_data,
    preprocess=preprocess,
    albumentations_transform=albumentations_transform,
    augment=True
)


# 테스트 데이터셋 (증강 미포함)
test_dataset = VideoFrameDataset(
    video_dir= '/kaggle/input/deepfake-detection-challenge/test_videos',
    df=test_data,
    preprocess=preprocess,
    albumentations_transform=None,
    augment=False
)

# 균형 샘플러 생성
train_sampler = create_balanced_sampler(train_dataset)

# DataLoader 생성
train_loader = DataLoader(train_dataset, batch_size=16, sampler=train_sampler)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

# 데이터 확인
print(f"훈련 데이터로더 샘플 크기: {len(train_loader)}")
print(f"테스트 데이터로더 샘플 크기: {len(test_loader)}")
