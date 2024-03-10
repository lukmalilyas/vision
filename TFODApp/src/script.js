// Check if browser supports speech recognition
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
  // Create a new SpeechRecognition object
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

  // Set recognition parameters
  recognition.lang = 'en-US'; // Set language to English (US)

  // Add event listener for when speech is recognized
  recognition.onresult = function(event) {
    const result = event.results[0][0].transcript.toLowerCase(); // Get recognized text
    console.log('Recognized speech: a', result);
    
    // Get the text content of the button
    const buttonText = document.getElementById('objectdetectionbutton1').textContent.toLowerCase();

    // Check if recognized speech matches the button text
    if (result.includes(buttonText)) {
      // Check if the recognized speech exactly matches the button text
      if (result.trim() === buttonText.trim()) {
        window.location.href = document.getElementById('objectdetectionbutton1').href; // Simulate button click
      }
    }
  };

  // Add event listener for errors
  recognition.onerror = function(event) {
    console.error('Speech recognition error: ', event.error);
  };

  // Start speech recognition
  recognition.start();

  // Add event listener for button click
} else {
  console.error('Speech recognition not supported.');
}