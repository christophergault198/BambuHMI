import tensorflow as tf
import numpy as np

# Load the model
new_model = tf.keras.models.load_model('Build_Plate_Detection.keras')

# Image dimensions
img_height, img_width = 180, 180 

# Show the model architecture
new_model.summary()

# Image URL
image_url = input("Enter the URL of the image: ")

# Download and load the image
image_path = tf.keras.utils.get_file('Red_Sunflower', origin=image_url)
img = tf.keras.utils.load_img(image_path, target_size=(img_height, img_width))
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create a batch

# Make predictions
predictions = new_model.predict(img_array)
score = tf.nn.softmax(predictions[0])

# Class names
class_names = ['itemoff', 'itemon']  # Assuming itemoff is class 0 and itemon is class 1

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
