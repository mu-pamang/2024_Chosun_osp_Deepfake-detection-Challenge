from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'deepfake_detection/home.html')

def upload_file(request):
    if request.method == 'POST':
        # 파일 업로드 시 처리(추후 모델 처리 코드 추가 예정)
        upload_file = request.FILES['file']
        # 모델 완성 시 파일을 처리하는 로직 추가 예정
        return HttpResponse("파일이 업로드됨.")
    return render(request, 'deepfake_detection/upload.html')