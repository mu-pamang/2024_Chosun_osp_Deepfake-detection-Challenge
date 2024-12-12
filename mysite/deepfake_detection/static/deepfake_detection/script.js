// document.getElementById('upload-form').addEventListener('submit', function(e) {
//     e.preventDefault();  // 폼의 기본 제출 동작을 막음
    
//     // CSRF 토큰을 가져오는 부분
//     const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
//     const videoInput = document.getElementById('video-input');
//     const formData = new FormData();
//     formData.append('video', videoInput.files[0]);

//     // fetch 요청으로 비디오 파일 업로드
//     fetch('/deepfake_detect/upload/', {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': csrfToken  // CSRF 토큰을 헤더에 추가
//         },
//         body: formData,  // FormData를 본문에 첨부
//     })
//     .then(response => response.json())  // JSON 응답을 파싱
//     .then(data => {
//         const resultDiv = document.getElementById('result');
//         if (data.suspect_frames) {
//             // 응답 데이터에서 의심되는 프레임을 표시
//             resultDiv.innerHTML = '의심되는 프레임: ' + data.suspect_frames.join(', ');
//         } else if (data.error) {
//             // 에러 메시지가 있다면 표시
//             resultDiv.innerHTML = '오류 발생: ' + data.error;
//         } else {
//             // 예상하지 못한 응답 처리
//             resultDiv.innerHTML = '알 수 없는 오류가 발생했습니다.';
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         // 네트워크 또는 서버 오류 처리
//         document.getElementById('result').innerHTML = '서버에 오류가 발생했습니다.';
//     });
// });


document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault(); // 폼 제출 방지

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const videoInput = document.getElementById('video-input');
    const videoPreview = document.getElementById('uploaded-video');
    const emptyVideoBox = document.getElementById('empty-video-box');
    const resultDiv = document.getElementById('result');

    if (videoInput.files.length === 0) {
        alert('비디오 파일을 선택해주세요.');
        return;
    }

    const formData = new FormData();
    formData.append('video', videoInput.files[0]);

    // 업로드한 비디오 미리보기
    videoPreview.src = URL.createObjectURL(videoInput.files[0]);
    videoPreview.style.display = 'block';
    emptyVideoBox.style.display = 'none';

    resultDiv.innerHTML = '<h2>분석 중입니다... 잠시만 기다려주세요.</h2>';

    fetch('/upload/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.label && data.confidence) {
                resultDiv.innerHTML = `
                    <h2>${data.label}</h2>
                    <div>Confidence: ${data.confidence}%</div>
                `;
            } else if (data.error) {
                resultDiv.innerHTML = `<h2>Error: ${data.error}</h2>`;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            resultDiv.innerHTML = '<h2>서버에 오류가 발생했습니다.</h2>';
        });
});

document.getElementById('clear-btn').addEventListener('click', function () {
    const videoInput = document.getElementById('video-input');
    const videoPreview = document.getElementById('uploaded-video');
    const emptyVideoBox = document.getElementById('empty-video-box');
    const resultDiv = document.getElementById('result');

    videoInput.value = '';
    videoPreview.src = '';
    videoPreview.style.display = 'none';
    emptyVideoBox.style.display = 'flex';
    resultDiv.innerHTML = '<h2>Upload a video to see the detection result.</h2>';
});



