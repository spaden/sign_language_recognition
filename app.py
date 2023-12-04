from flask import Flask, request, jsonify
import os
from flask_cors import CORS, cross_origin

import cv2
import numpy as np
from tensorflow import keras
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
port = 5100

model = keras.models.load_model("104labels.h5")


def preprocess_image(base64_str, target_size=(128, 128)):
    try:
        # Decode base64 string into image
        base64_content = base64_str.split(",")[1] if "," in base64_str else base64_str

        img_data = base64.b64decode(base64_content)
        img = Image.open(BytesIO(img_data))
        img = np.array(img)

        # Resize and normalize the image
        img = cv2.resize(img, target_size)
        img = img / 255.0

        # Reshape the image to match the model's input shape.
        input_image = np.expand_dims(img, axis=0)
        return input_image
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
        predictions = model.predict(processed_img)
        print(predictions)
        predicted_class_index = np.argmax(predictions)
        print(predicted_class_index)
        classes = ['eat', 'friends', 'help', 'me', 'play', 'thankyou', 'what', 'where', 'who', 'why', 'Hello',
                   'iloveyou', 'yes']

        predicted_class = classes[predicted_class_index]  # Map index to class label

        print(f"The model predicts the image contains: {predicted_class}")

    return jsonify({'data': predicted_class})



if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8004', threaded=True)