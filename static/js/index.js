const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const outputDiv = document.getElementById('output');
const constraints = {
    video: true
};

async function initCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
    } catch (err) {
        console.error('Error accessing the webcam: ', err);
    }
}

function speak(text) {
    var speech = new SpeechSynthesisUtterance();
    speech.text = text;
    
    window.speechSynthesis.speak(speech);
  }

function captureImage() {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');

    // Send captured image to server
    fetch('/upload', {
        method: 'POST',
        body: JSON.stringify({ image: imageData }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.text())
    .then(text => {
        speak(text)
        outputDiv.innerText = text;
    })
    .catch(error => console.error('Error sending image to server: ', error));
}

initCamera();

captureButton.addEventListener('click', captureImage);