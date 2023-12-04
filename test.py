

import cv2
import numpy as np
from tensorflow import keras

# Load the trained model.
model = keras.models.load_model("104labels.h5")

# Load and preprocess the test image.
test_image_path = "what_4.jpg"
IMAGE_SIZE = (128, 128)

img = cv2.imread(test_image_path)
img = cv2.resize(img, IMAGE_SIZE)
img = img / 255.0  # Normalize pixel values to [0, 1]

# Reshape the image to match the model's input shape.
input_image = np.expand_dims(img, axis=0)

# Make predictions with the model.
predictions = model.predict(input_image)

print(predictions)
# Interpret the model's predictions.
predicted_class_index = np.argmax(predictions)
print(predicted_class_index)
classes = ['eat','friends','help','me','play','thankyou','what','where','who','why','Hello','iloveyou','yes']


predicted_class = classes[predicted_class_index]  # Map index to class label

print(f"The model predicts the image contains: {predicted_class}")
