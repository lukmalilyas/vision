
    // More API functions here:
    // https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/image

    // the link to your model provided by Teachable Machine export panel
    const modelURL = "https://visioncookingapplication2.s3.ap-south-1.amazonaws.com/tm-my-image-model/model.json";
    const metadataURL = "https://visioncookingapplication2.s3.ap-south-1.amazonaws.com/tm-my-image-model/metadata.json";

    let model, webcam, labelContainer, maxPredictions;

    // Load the image model and setup the webcam
    async function init() {

        // load the model and metadata
        // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
        // or files from your local hard drive
        // Note: the pose library adds "tmImage" object to your window (window.tmImage)
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
        await predict();
        window.requestAnimationFrame(loop);
    }

    // run the webcam image through the image model
    let spokenPrediction = {};

    async function predict() {
        const prediction = await model.predict(webcam.canvas);
        for (let i = 0; i < maxPredictions; i++) {
            const classPrediction = prediction[i].className;
            const probability = prediction[i].probability.toFixed(2);
    
            labelContainer.childNodes[i].innerHTML = `${classPrediction}: ${probability}`;
    
            if (probability > 0.9 && !spokenPrediction[classPrediction]) {
                spokenPrediction[classPrediction] = true;
                speak(classPrediction);
            } else if (probability <= 0.9) {
                spokenPrediction[classPrediction] = false;
            }
        }
        window.requestAnimationFrame(loop);
    }

    function speak(text) {
        text = text.replace(/_/g, ' ');
        // Create a new SpeechSynthesisUtterance object with the provided text
        const utterance = new SpeechSynthesisUtterance(text);
        // Speak the text
        window.speechSynthesis.speak(utterance);
    }

    init();
