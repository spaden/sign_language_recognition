from flask import Flask, request, jsonify
import os
from flask_cors import CORS, cross_origin

import cv2
import numpy as np
from tensorflow import keras
import base64
from io import BytesIO
from PIL import Image

import json

app = Flask(__name__)
port = 5100

model = keras.models.load_model("latest_new.h5")


with open('class_indices.json', 'r') as json_file:
    class_indices = json.load(json_file)



def preprocess_image(base64_str, target_size=(128, 128)):
    try:
        # Decode base64 string into image
        base64_content = base64_str.split(",")[1] if "," in base64_str else base64_str

        img_data = base64.b64decode(base64_content)
        img = Image.open(BytesIO(img_data))
        img = np.array(img)

        # Resize and normalize the image
        img = cv2.resize(img, target_size)
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian Blur
        blur = cv2.GaussianBlur(gray, (5, 5), 2)

        # Adaptive Thresholding
        th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Global Thresholding using Otsu's method
        ret, result_mask = cv2.threshold(th3, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Expand dimensions to match model input dimensions
        result_mask = np.expand_dims(result_mask, axis=-1)

        # Normalize the image
        result_mask = result_mask / 255.0

        # Reshape to match the input shape expected by the model
        result_mask = np.reshape(result_mask, (1, 128, 128, 1))

        return result_mask

    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

@app.route("/")
@cross_origin() # allow all origins all methods.
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route('/upload', methods=['POST'])
@cross_origin(origin='*')
def upload_images():
    if request:
        data = request.json
        imgs = data['image']
        processed_img = preprocess_image(imgs)

        result = model.predict(processed_img)
        print(np.argmax(result))
        # Get the predicted class index

        predicted_label = [label for label, index in class_indices.items() if index == np.argmax(result)][0]

        #print(predicted_label)

    return jsonify({'data': predicted_label})
