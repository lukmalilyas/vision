from flask import Flask, render_template, request, jsonify
from speech_to_text import recognize_speech
import requests
import subprocess


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


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
