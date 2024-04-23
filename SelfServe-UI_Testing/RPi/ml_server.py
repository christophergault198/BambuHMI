from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load the model
new_model = tf.keras.models.load_model('MODEL_NAME.h5')

# Image dimensions
img_height, img_width = 224, 224

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image from the request
    image = Image.open(io.BytesIO(request.files['image'].read()))
    image = image.resize((img_height, img_width))
    image = np.array(image) / 255.0  # Normalize the image

    # Make predictions
    predictions = new_model.predict(np.expand_dims(image, axis=0))
    predicted_class = np.argmax(predictions)

    # Return the predictions
    return jsonify({'class': int(predicted_class)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Added debug=True for development purposes
