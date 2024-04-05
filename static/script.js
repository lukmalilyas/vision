// Check if browser supports speech recognition
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
  // Create a new SpeechRecognition object
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

  // Set recognition parameters
  recognition.lang = 'en-US'; // Set language to English (US)

  // Add event listener for when speech is recognized
  recognition.onresult = function(event) {
    let result = event.results[0][0].transcript.toLowerCase(); // Get recognized text
    console.log('Recognized speech:', result);
    
    result = result.replace(/\./g, '');

    if (result.trim() === "object detection") {
      window.location.href = document.getElementById('objectdetectionbutton1').href; // Simulate button click
    }
    else if(result.trim() === "home") {
      window.location.href = document.getElementById('objectdetectionbutton0').href; // Simulate button click
    }
    else if(result.trim() === "recipe recommendation") {
      window.location.href = document.getElementById('objectdetectionbutton3').href; // Simulate button click
    }
    else if(result.trim() === "chat bot") {
      window.location.href = document.getElementById('objectdetectionbutton2').href; // Simulate button click
    }
    else if(result.trim() === "label reader") {
      window.location.href = document.getElementById('objectdetectionbutton4').href; // Simulate button click
    }
  };

  // Add event listener for errors
  recognition.onerror = function(event) {
    console.error('Speech recognition error:', event.error);
  };

  // Start speech recognition
  recognition.start();

  // Add event listener for button click

  // Continuously restart speech recognition
  recognition.onend = function() {
    console.log('Speech recognition ended. Restarting...');
    recognition.start();
  };
} else {
  console.error('Speech recognition not supported.');
}
