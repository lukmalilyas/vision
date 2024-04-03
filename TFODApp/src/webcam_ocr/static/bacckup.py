from flask import Flask, render_template, request, jsonify
import base64
from PIL import Image
from io import BytesIO
from pytesseract import pytesseract
import cv2
import os
import numpy as np

# Path to the Tesseract executable
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

# Initialize Flask app
app = Flask(__name__)

# Function to perform text detection using Tesseract
def tesseract():
    image_path = r"D:\Youtube\TensorFlow Object Detection\TFODApp\test1.jpg"
    text = pytesseract.image_to_string(Image.open(image_path))
    print(text)
    return text

@app.route('/')
def index():
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

        
        return jsonify({'text': text})
    else:
        return 'Only POST requests are allowed for this endpoint.'

if __name__ == '__main__':
    app.run(debug=True)
