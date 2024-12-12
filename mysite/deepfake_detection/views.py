## 세린님이 작성하신 cv2로 출력하는 코드
# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# import cv2
# import os
# import tempfile

# # 홈 페이지 뷰
# def home(request):
#     return render(request, 'deepfake_detection/home.html')

# # 비디오 파일 업로드 및 분석 처리 뷰
# def upload_file(request):
#     if request.method == 'POST' and request.FILES.get('video'):
#         # 파일 업로드 처리
#         video_file = request.FILES['video']
        
#         # 임시 비디오 파일 경로 생성
#         video_path = tempfile.mktemp(suffix='.mp4')
        
#         # 업로드된 비디오 파일을 임시 파일에 저장
#         with open(video_path, 'wb') as f:
#             for chunk in video_file.chunks():
#                 f.write(chunk)
        
#         # 비디오에서 프레임 추출 및 분석
#         video_capture = cv2.VideoCapture(video_path)
#         frames = []
#         suspect_frames = []
#         frame_count = 0
        
#         while True:
#             ret, frame = video_capture.read()
#             if not ret:
#                 break
#             frames.append(frame)
#             # 예시: 10번째마다 의심되는 프레임을 추가 (실제 분석 로직은 여기에 추가)
#             if frame_count % 10 == 0:
#                 suspect_frames.append(frame_count)
#             frame_count += 1
        
#         video_capture.release()
#         os.remove(video_path)  # 임시 파일 삭제
        
#         # 의심되는 프레임 리스트 반환
#         return JsonResponse({'suspect_frames': suspect_frames})

#     # GET 요청일 경우 업로드 폼을 보여줌
#     return render(request, 'deepfake_detection/upload.html')



## 비디오 파일 하나 넣고 결과 값 출력하는 코드
from django.shortcuts import render
from django.http import JsonResponse
import os
import tempfile
import requests

# 홈 페이지 뷰
def home(request):
    return render(request, 'deepfake_detection/home.html')

# 비디오 파일 업로드 및 코랩 연동 처리 뷰
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']

        # 임시 파일 저장
        temp_video_path = tempfile.mktemp(suffix='.mp4')
        with open(temp_video_path, 'wb') as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        # 코랩 서버로 요청 보내기
        colab_url = "http://<colab-server-ip>:<port>/predict"  # 코랩 서버 주소
        try:
            with open(temp_video_path, 'rb') as f:
                response = requests.post(colab_url, files={'video': f})

            # 응답 처리
            os.remove(temp_video_path)  # 임시 파일 삭제
            if response.status_code == 200:
                result = response.json()
                return JsonResponse(result)
            else:
                return JsonResponse({'error': 'Failed to get a response from Colab.'}, status=500)
        except Exception as e:
            os.remove(temp_video_path)  # 에러 발생 시 파일 삭제
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method or no file uploaded.'}, status=400)
