import os
import tensorflow as tf
import numpy as np
from PIL import ImageFile

# Load the model
new_model = tf.keras.models.load_model('Build_Plate_Detection.keras')

# Image dimensions
img_height, img_width = 224, 224

# Define class names
class_names = ['itemoff', 'itemon']  # itemoff is class 0 and itemon is class 1

def predict(image_path):
    """
    Predict the class of an image given its file path.

    Args:
    image_path (str): The path to the image file.

    Returns:
    dict: A dictionary containing the predicted class label and confidence.
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    # Load the image
    img = tf.keras.utils.load_img(image_path, target_size=(img_height, img_width))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Make predictions
    predictions = new_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Get the predicted class
    predicted_class_index = np.argmax(score)
    predicted_class_label = class_names[predicted_class_index]
    confidence = 100 * np.max(score)
    print(predicted_class_label, confidence)
    return {
        "predicted_class": predicted_class_label,
        "confidence": f"{confidence:.2f}%"
    }

# Example usage (comment out or remove in production)
# if __name__ == "__main__":
#     result = predict('path_to_your_image.jpg')
#     print(result)
