import os
import random
import tensorflow as tf
import numpy as np

# Load the model
new_model = tf.keras.models.load_model('Build_Plate_Detection.keras')

# Image dimensions
img_height, img_width = 224, 224  

# Show the model architecture
new_model.summary()

# Define the folder containing the images
folder_path = "toolhead_images"

# List all files in the folder
image_files = os.listdir(folder_path)

# Randomly select two images
random_images = random.sample(image_files, 10)

for image_file in random_images:
    # Load the image
    image_path = os.path.join(folder_path, image_file)
    img = tf.keras.utils.load_img(image_path, target_size=(img_height, img_width))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Make predictions
    predictions = new_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Class names
    class_names = ['itemon', 'itemoff']  # itemoff is class 0 and itemon is class 1

    print("Image:", image_file)
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )
    print()
