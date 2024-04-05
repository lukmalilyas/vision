from flask import Flask, render_template, request, jsonify
from speech_to_text import recognize_speech
import requests
import subprocess
import base64
import easyocr


RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'
app = Flask(__name__, static_url_path='/static')


# Function to start Rasa server as subprocess
def start_rasa_server():
    try:
        subprocess.Popen(['rasa', 'run', 'actions'])
        subprocess.Popen(['rasa', 'run'])
    except Exception as e:
        print(f"Error starting Rasa server: {e}")


# Start Rasa server when Flask app is initialized
start_rasa_server()


@app.route('/')
def chatbot():
    return render_template('chatbot.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    modified_text = None
    while modified_text is None:
        modified_text = recognize_speech()
        if modified_text:
            break

    if modified_text:
        return jsonify({'text': modified_text}), 200
    else:
        return jsonify({'error': 'Failed to transcribe'}), 500


@app.route('/rasa', methods=['POST'])
def rasa():
    data = request.json
    text = data['text']

    # Send text to Rasa
    response = requests.post(RASA_API_URL, json={"message": text})

    if response.ok:
        # Extract the response from Rasa
        rasa_response = response.json()
        bot_response = [message['text'] for message in rasa_response] if rasa_response else ['Sorry, I didn\'t understand that.']
        return jsonify({'response': bot_response}), 200
    else:
        return jsonify({'error': 'Failed to get response from Rasa'}), 500


# Function to perform text detection using Tesseract
def tesseract():
    image_path = "C:/Users/muham/OneDrive/Desktop/CM2603/Project/Chatbot/Cooking_bot/test1.jpg"
    reader = easyocr.Reader(['en'], gpu=False)
    text = reader.readtext(image_path)
    text = text[0][1]
    print(text)
    return text


@app.route('/label_reader')
def label_reader():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        data = request.json
        image_data = data['image'].split(',')[1]  # Extract base64 image data

        # Decode and save the image locally as "test1.jpg"
        img_data = base64.b64decode(image_data)
        with open("test1.jpg", "wb") as f:
            f.write(img_data)

        text = tesseract()

        return jsonify(text)
    else:
        return 'Only POST requests are allowed for this endpoint.'


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
