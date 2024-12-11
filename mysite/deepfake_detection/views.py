from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import cv2
import os
import tempfile

# 홈 페이지 뷰
def home(request):
    return render(request, 'deepfake_detection/home.html')

# 비디오 파일 업로드 및 분석 처리 뷰
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('video'):
        # 파일 업로드 처리
        video_file = request.FILES['video']
        
        # 임시 비디오 파일 경로 생성
        video_path = tempfile.mktemp(suffix='.mp4')
        
        # 업로드된 비디오 파일을 임시 파일에 저장
        with open(video_path, 'wb') as f:
            for chunk in video_file.chunks():
                f.write(chunk)
        
        # 비디오에서 프레임 추출 및 분석
        video_capture = cv2.VideoCapture(video_path)
        frames = []
        suspect_frames = []
        frame_count = 0
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            frames.append(frame)
            # 예시: 10번째마다 의심되는 프레임을 추가 (실제 분석 로직은 여기에 추가)
            if frame_count % 10 == 0:
                suspect_frames.append(frame_count)
            frame_count += 1
        
        video_capture.release()
        os.remove(video_path)  # 임시 파일 삭제
        
        # 의심되는 프레임 리스트 반환
        return JsonResponse({'suspect_frames': suspect_frames})

    # GET 요청일 경우 업로드 폼을 보여줌
    return render(request, 'deepfake_detection/upload.html')
