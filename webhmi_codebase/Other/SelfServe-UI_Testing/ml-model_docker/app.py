from flask import Flask, request, jsonify
import Prediction  # Assuming Prediction.py is adjusted to be used as a module

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Receive the image file
    file = request.files['image']
    # Save the image to a temporary file or directly pass the image stream to the prediction logic
    image_path = 'temp_image.jpg'
    file.save(image_path)
    
    # Run prediction (assuming Prediction.py is modified to accept an image path and return a prediction)
    prediction = Prediction.predict(image_path)
    
    # Return the prediction result
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)