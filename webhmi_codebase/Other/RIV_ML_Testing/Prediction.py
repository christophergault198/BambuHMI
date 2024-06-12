import os
import tensorflow as tf
import numpy as np
from PIL import ImageFile

# Load the model
new_model = tf.keras.models.load_model('Build_Plate_Detection.keras')

# Image dimensions
img_height, img_width = 224, 224

# Show the model architecture
new_model.summary()

# Define the folder containing the images
folder_path = "toolhead_images"

# List all files in the folder and find the most recent one
image_files = os.listdir(folder_path)
most_recent_image = max(image_files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Load the most recent image
image_path = os.path.join(folder_path, most_recent_image)
img = tf.keras.utils.load_img(image_path, target_size=(img_height, img_width))
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create a batch

# Make predictions
predictions = new_model.predict(img_array)
score = tf.nn.softmax(predictions[0])

# Get the predicted class
predicted_class_index = np.argmax(score)
class_names = ['itemoff', 'itemon']  # itemoff is class 0 and itemon is class 1
predicted_class_label = class_names[predicted_class_index]
print(most_recent_image)
print(
    "The most recent image most likely belongs to {} with a {:.2f} percent confidence."
    .format(predicted_class_label, 100 * np.max(score))
)

