import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image

# Function to load the Keras model
def load_model(model_path):
   
    try:
        model = keras.models.load_model(model_path)
        print(f"Model loaded successfully from: {model_path}")
        return model
    except OSError as e:
        print(f"Error loading model: {e}")
        return None

def preprocess_image(image_path, target_size=(180, 180)):
    img = image.load_img(image_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize pixel values to [0, 1]
    img_array = tf.expand_dims(img_array, axis=0)  # Add a batch dimension
    return img_array

# Function to make predictions using the model
def predict(model, image_path):
    preprocessed_image = preprocess_image(image_path)
    predictions = model.predict(preprocessed_image)

    # Assuming it's a classification model
    predicted_class_index = tf.argmax(predictions[0])
    predicted_probability = tf.nn.softmax(predictions[0])[predicted_class_index].numpy()

    return [f"Predicted class index: {predicted_class_index}", f"Probability: {predicted_probability:.4f}"]

if __name__ == "__main__":
    # Load the Keras model (replace with your actual model path)
    model = load_model("Build_Plate_Detection.keras")

    if model is not None:
        # Get user input for image path
        image_path = input("Enter the path to your image: ")

        # Make predictions
        predictions = predict(model, image_path)
        print("Predictions:")
        for prediction in predictions:
            print(prediction)
