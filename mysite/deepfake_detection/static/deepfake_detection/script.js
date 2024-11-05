document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const videoInput = document.getElementById('video-input');
    const formData = new FormData();
    formData.append('video', videoInput.files[0]);

    try {
        const response = await fetch('/api/detect/', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        document.getElementById('result').innerText = data.result || 'Error occurred.';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerText = '오류가 발생했습니다.';
    }
});