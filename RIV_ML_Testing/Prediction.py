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

# Randomly select ten images
random_images = random.sample(image_files, 10)

# Initialize variables to accumulate confidence scores
total_scores = [0.0, 0.0] 

for image_file in random_images:
    # Load the image
    image_path = os.path.join(folder_path, image_file)
    img = tf.keras.utils.load_img(image_path, target_size=(img_height, img_width))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Make predictions
    predictions = new_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

<<<<<<< Updated upstream
    # Accumulate confidence scores
    total_scores += score.numpy()
=======
    # Class names
    class_names = ['itemon', 'itemoff']  # itemoff is class 1 and itemon is class 0 
>>>>>>> Stashed changes

# Calculate average confidence scores
average_scores = total_scores / len(random_images)

# Get the predicted class
predicted_class_index = np.argmax(average_scores)
class_names = ['itemoff', 'itemon']  # itemoff is class 0 and itemon is class 1
predicted_class_label = class_names[predicted_class_index]

print(
    "The images most likely belong to {} with a {:.2f} percent confidence."
    .format(predicted_class_label, 100 * np.max(average_scores))
)
