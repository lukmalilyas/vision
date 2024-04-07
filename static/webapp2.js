const modelURL = "https://visioncookingapplication2.s3.ap-south-1.amazonaws.com/tm-my-image-model/model.json";
const metadataURL = "https://visioncookingapplication2.s3.ap-south-1.amazonaws.com/tm-my-image-model/metadata.json";

let model, webcam, labelContainer, maxPredictions;
let lastPredictionTime = 0;
const predictionInterval = 5000; // 5000 milliseconds (5 seconds) interval between predictions

// Load the image model and setup the webcam
async function init() {
    model = await tmImage.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    // Convenience function to setup a webcam
    const flip = true; // whether to flip the webcam
    webcam = new tmImage.Webcam(700, 400, flip); // width, height, flip
    await webcam.setup(); // request access to the webcam
    await webcam.play();
    window.requestAnimationFrame(loop);

    // append elements to the DOM
    document.getElementById("webcam-container").appendChild(webcam.canvas);
    labelContainer = document.getElementById("label-container");
    for (let i = 0; i < maxPredictions; i++) { // and class labels
        labelContainer.appendChild(document.createElement("div"));
    }
}

async function loop() {
    webcam.update(); // update the webcam frame
    const currentTime = Date.now();
    if (currentTime - lastPredictionTime >= predictionInterval) {
        lastPredictionTime = currentTime;
        await predict();
    }
    window.requestAnimationFrame(loop);
}

// run the webcam image through the image model
async function predict() {
    // predict can take in an image, video or canvas html element
    const prediction = await model.predict(webcam.canvas);
    for (let i = 0; i < maxPredictions; i++) {
        const classPrediction =
            prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        labelContainer.childNodes[i].innerHTML = classPrediction;
        if (prediction[i].probability.toFixed(2) > 0.9) {
            const spokenPrediction = prediction[i].className.replace(/_/g, ' ');
            speak(spokenPrediction);
        }
    }
}

function speak(text) {
    // Create a new SpeechSynthesisUtterance object with the provided text
    const utterance = new SpeechSynthesisUtterance(text);
    // Speak the text
    window.speechSynthesis.speak(utterance);
}

init();
