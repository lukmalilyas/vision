document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event triggered');
    const recordButton = document.getElementById('record-button');
    const chatbox = document.getElementById('chatbox');
    let isListening = false;

    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.lang = 'en-US';

    recognition.onstart = function() {
        console.log('Speech recognition started');
        isListening = true;
    };

    recognition.onend = function() {
        console.log('Speech recognition ended');
        if (isListening) {
            recognition.start();
        }
    };

    recognition.onresult = function(event) {
        console.log('Speech recognition result:', event);
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript.trim();
            const phrase_1 = 'Chatbot'
            const phrase_2 = 'Chat bot'
            console.log('Transcript:', transcript.trim());
            if (transcript.includes(phrase_1) || transcript.includes(phrase_2)) {
                console.log('Transcript matched:', transcript);
                recognition.stop();
                speechSynthesis.speak(new SpeechSynthesisUtterance("Listening..."));
                recordButton.click();
                break;
            } else if (transcript.toLowerCase().includes('home')) {
                window.location.href = "http://127.0.0.1:5000/static/Home.html";
            } else if (transcript.toLowerCase().includes('object detection')) {
                window.location.href = "http://127.0.0.1:5000/static/objectdetectionapp.html";
            } else if (transcript.toLowerCase().includes('label reader')) {
                window.location.href = "http://127.0.0.1:5000/label_reader";
            } else if (transcript.toLowerCase().includes('recipe recommendation')) {
                window.location.href = "http://127.0.0.1:5000/static/recipeRecom.html";
            }
        }
    };

    recognition.start();

    recordButton.addEventListener('click', async () => {
        console.log('Record button clicked');
        try {
            const response = await fetch('/transcribe', { method: 'POST' });
            const data = await response.json();

            if (response.ok) {
                appendMessageAndResponse(data.text);
                sendToRasa(data.text)
                recognition.start();
            } else {
                console.error('Error:', data.error);
                recognition.start();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    async function sendToRasa(text) {
        try {
            const response = await fetch('/rasa', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });
            const data = await response.json();

            if (response.ok) {
                appendMessageAndResponse(null, data.response);
            } else {
                console.error('Error:', data.error);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function appendMessageAndResponse(question, response) {
        console.log('Appending message and response:', question, response);

        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container');

        if (question) {
            const userQuestion = document.createElement('div');
            userQuestion.classList.add('right-part');
            const chatbotChart = document.createElement('div');
            chatbotChart.classList.add('chatbot-chart');
            const userIcon = document.createElement('i');
            userIcon.classList.add('bx', 'bx-user');
            const userText = document.createElement('p');
            userText.textContent = question;
            const timestamp = document.createElement('span');
            timestamp.textContent = getCurrentTime()
            chatbotChart.appendChild(userIcon);
            chatbotChart.appendChild(userText);
            chatbotChart.appendChild(timestamp)
            userQuestion.appendChild(chatbotChart)
            messageContainer.appendChild(userQuestion);
        }

        if (response) {
            const chatbotResponse = document.createElement('div');
            chatbotResponse.classList.add('left-part');
            const agentChart = document.createElement('div');
            agentChart.classList.add('agent-chart');
            const agentIcon = document.createElement('i');
            agentIcon.classList.add('fa-solid', 'fa-robot');
            const agentText = document.createElement('p');
            agentText.textContent = response;
            agentChart.appendChild(agentIcon);
            agentChart.appendChild(agentText);
            chatbotResponse.appendChild(agentChart);
            messageContainer.appendChild(chatbotResponse);

            const utterance = new SpeechSynthesisUtterance(response);
            speechSynthesis.speak(utterance);
        }

        chatbox.appendChild(messageContainer);
    }

    function getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
});