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
def tesseract(image_data):
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    text = pytesseract.image_to_string(image)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        data = request.json
        image_data = data['image'].split(',')[1]  # Extract base64 image data
        
        # Save the image as "test1.jpg"
        img = Image.open(BytesIO(base64.b64decode(image_data)))
        img.save("test1.jpg")
        
        text = tesseract(image_data)
        
        # Convert base64 image data to OpenCV format
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Display the image using OpenCV
        cv2.imshow('Captured Image', img_cv2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return jsonify({'text': text})
    else:
        return 'Only POST requests are allowed for this endpoint.'

if __name__ == '__main__':
    app.run(debug=True)
