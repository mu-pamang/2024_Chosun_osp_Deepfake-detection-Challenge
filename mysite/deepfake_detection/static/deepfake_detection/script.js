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

/* document.getElementById('upload-form').addEventListener('submit', function (e) {
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

function previewVideo(event) {
    const video = document.getElementById('video-preview');
    const fileNameSpan = document.getElementById('file-name');
    const fileInput = event.target.files[0];

    if (fileInput) {
        video.src = URL.createObjectURL(fileInput);
        video.load();
        video.play();
        fileNameSpan.textContent = fileInput.name; // Display selected file name
    }
}

function clearAll() {
    document.getElementById('video-preview').src = "";
    document.querySelector('.video-input').value = "";
    document.getElementById('output-area').innerHTML = "Detection results will appear here.";
    document.getElementById('file-name').textContent = "No file selected"; // Reset file name
}

function submitVideo() {
    document.getElementById('output-area').innerHTML = "Processing video...";
}


function previewVideo(event) {
    const video = document.getElementById('video-preview'); // 비디오 미리보기 엘리먼트
    const fileNameSpan = document.getElementById('file-name'); // 선택한 파일 이름 표시
    const fileInput = event.target.files[0]; // 업로드한 파일

    if (fileInput) {
        video.src = URL.createObjectURL(fileInput); // 로컬 미리보기 URL 생성
        video.load();
        video.play();
        fileNameSpan.textContent = fileInput.name; // 선택한 파일 이름 업데이트
    }
}

function clearAll() {
    const video = document.getElementById('video-preview');
    const fileNameSpan = document.getElementById('file-name');
    const outputArea = document.getElementById('output-area');
    const videoInput = document.querySelector('.video-input');

    // 미리보기 초기화
    video.src = "";
    videoInput.value = ""; // 파일 입력 초기화
    fileNameSpan.textContent = "No file selected"; // 파일 이름 초기화
    outputArea.textContent = "Detection results will appear here."; // 출력 영역 초기화
}

function submitVideo() {
    const outputArea = document.getElementById('output-area');

    // 제출 상태 알림
    outputArea.textContent = "Processing video...";
} */

/* document.addEventListener('DOMContentLoaded', function () {
    // DOM 요소 가져오기
    const videoInput = document.getElementById('video-input');
    const videoPreview = document.getElementById('video-preview');
    const fileNameSpan = document.getElementById('file-name');
    const outputArea = document.getElementById('output-area');
    const clearButton = document.getElementById('clear-btn');
    const submitButton = document.getElementById('submit-btn');
    const editButton = document.getElementById('edit-btn');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    // 비디오 파일 선택 시 미리보기
    videoInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            videoPreview.src = URL.createObjectURL(file);
            videoPreview.load();
            videoPreview.play();
            fileNameSpan.textContent = file.name; // 파일 이름 표시
            outputArea.textContent = "Detection results will appear here."; // 결과 초기화
        } else {
            clearAll();
        }
    });

    // "EDIT" 버튼 클릭 시 파일 선택 창 열기
    editButton.addEventListener('click', function () {
        videoInput.click();
    });
    
    // CLEAR 버튼 클릭 시 초기화
    clearButton.addEventListener('click', function () {
        clearAll();
    });

    // SUBMIT 버튼 클릭 시 서버로 파일 전송
    submitButton.addEventListener('click', function () {
        if (!videoInput.files.length) {
            alert('비디오 파일을 선택해주세요.');
            return;
        }
    
        outputArea.textContent = 'Processing video...';

        const formData = new FormData();
        formData.append('video', videoInput.files[0]);

        fetch('/upload/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken || '', // CSRF 토큰 추가
            },
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.label && data.confidence) {
                    outputArea.innerHTML = `
                        <h2>${data.label}</h2>
                        <div>Confidence: ${data.confidence}%</div>
                    `;
                } else if (data.error) {
                    outputArea.innerHTML = `<h2>Error: ${data.error}</h2>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                outputArea.textContent = '서버에 오류가 발생했습니다.';
            });
    });

    // 모든 필드를 초기화하는 함수
    function clearAll() {
        videoPreview.src = ''; // 비디오 미리보기 초기화
        videoInput.value = ''; // 파일 입력 초기화
        fileNameSpan.textContent = 'No file selected'; // 파일 이름 초기화
        outputArea.textContent = 'Detection results will appear here.'; // 출력 영역 초기화
    }
}); */

// Form 제출 이벤트 핸들러
document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault(); // 기본 폼 제출 방지

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const videoInput = document.getElementById('video-input');
    const videoPreview = document.getElementById('uploaded-video');
    const emptyVideoBox = document.getElementById('empty-video-box');
    const resultDiv = document.getElementById('result');

    // 비디오 파일 선택 여부 확인
    if (videoInput.files.length === 0) {
        alert('비디오 파일을 선택해주세요.');
        return;
    }

    // FormData 생성 및 비디오 파일 추가
    const formData = new FormData();
    formData.append('video', videoInput.files[0]);

    // 비디오 미리보기 업데이트
    updateVideoPreview(videoInput.files[0], videoPreview, emptyVideoBox);

    // 결과 영역 초기화
    resultDiv.innerHTML = '<h2>분석 중입니다... 잠시만 기다려주세요.</h2>';

    // 비디오 업로드 및 결과 처리
    fetch('/upload/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => handleUploadResult(data, resultDiv))
        .catch((error) => handleUploadError(error, resultDiv));
});

// Clear 버튼 클릭 이벤트 핸들러
document.getElementById('clear-btn').addEventListener('click', clearForm);

// 비디오 미리보기 업데이트 함수
function updateVideoPreview(file, videoPreview, emptyVideoBox) {
    videoPreview.src = URL.createObjectURL(file);
    videoPreview.style.display = 'block';
    emptyVideoBox.style.display = 'none';
}

// 업로드 결과 처리 함수
function handleUploadResult(data, resultDiv) {
    if (data.label && data.confidence) {
        resultDiv.innerHTML = `
            <h2>${data.label}</h2>
            <div>Confidence: ${data.confidence}%</div>
        `;
    } else if (data.error) {
        resultDiv.innerHTML = `<h2>Error: ${data.error}</h2>`;
    }
}

// 업로드 에러 처리 함수
function handleUploadError(error, resultDiv) {
    console.error('Error:', error);
    resultDiv.innerHTML = '<h2>서버에 오류가 발생했습니다.</h2>';
}

// Clear 버튼 동작 함수
function clearForm() {
    const videoInput = document.getElementById('video-input');
    const videoPreview = document.getElementById('uploaded-video');
    const emptyVideoBox = document.getElementById('empty-video-box');
    const resultDiv = document.getElementById('result');

    videoInput.value = '';
    videoPreview.src = '';
    videoPreview.style.display = 'none';
    emptyVideoBox.style.display = 'flex';
    resultDiv.innerHTML = '<h2>Upload a video to see the detection result.</h2>';
}

// 독립적으로 사용할 수 있는 비디오 프리뷰 함수
function previewVideo(event) {
    const video = document.getElementById('video-preview');
    const fileNameSpan = document.getElementById('file-name');
    const fileInput = event.target.files[0];

    if (fileInput) {
        video.src = URL.createObjectURL(fileInput);
        video.load();
        video.play();
        fileNameSpan.textContent = fileInput.name; // 선택한 파일 이름 표시
    }
}