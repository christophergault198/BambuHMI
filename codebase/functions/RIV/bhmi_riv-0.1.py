import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import paramiko
from io import BytesIO
import os
from datetime import datetime
import hashlib
import torch
from torchvision import models, transforms
import threading  # Import the threading module

# Load a pre-trained Faster R-CNN model
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()  # Set the model to evaluation mode

# Define a transformation to prepare the image
transform = transforms.Compose([
    transforms.ToTensor(),
])

def detect_objects(image):
    # Transform the image and add a batch dimension
    image_tensor = transform(image).unsqueeze(0)
    
    # Get predictions
    with torch.no_grad():
        predictions = model(image_tensor)
    
    return predictions[0]

def draw_boxes(image, predictions):
    draw = ImageDraw.Draw(image)
    for element in predictions['boxes']:
        box = element.numpy()
        draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline="red", width=3)
    return image

# Global variable to store the hash of the last saved image
last_image_hash = None

def process_image(image_data):
    global last_image_hash
    # Convert the image data to a PIL Image
    image = Image.open(BytesIO(image_data))

    # Detect objects in the image
    predictions = detect_objects(image)

    # Draw bounding boxes on the image
    image_with_boxes = draw_boxes(image, predictions)

    # Convert the modified image to a format that Tkinter can use
    tk_image = ImageTk.PhotoImage(image_with_boxes)

    # Update the UI in the main thread
    def update_ui():
        image_label.configure(image=tk_image)
        image_label.image = tk_image  # Keep a reference!
    
    # Schedule the UI update to be run in the main thread
    root.after(0, update_ui)

def fetch_image():
    global last_image_hash  # Use the global variable to track the hash

    # SSH details
    ssh_host = '192.168.9.78' #CHANGE ME
    ssh_port = 22
    ssh_user = 'root'
    ssh_password = 'a8d11ef407b8' #CHANGE ME
    remote_file_path = '/userdata/log/cam/capture/calib_14.jpg'

    # Establish an SSH client and connect to the server
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

    # Use SSH client to fetch the remote file
    sftp = ssh.open_sftp()
    remote_file = sftp.file(remote_file_path, "rb")
    image_data = remote_file.read()
    remote_file.close()

    # Close the SSH connection
    ssh.close()

    # Calculate the hash of the fetched image data
    current_image_hash = hashlib.md5(image_data).hexdigest()

    # Check if the fetched image is different from the last saved image
    if current_image_hash != last_image_hash:
        # Update the last_image_hash
        last_image_hash = current_image_hash

        # Save the image data to a file in the specified folder
        save_folder = 'toolhead_images'  # Specify your folder path here
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        # Generate a unique filename for each image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'image_{timestamp}.jpg'
        file_path = os.path.join(save_folder, filename)
        with open(file_path, 'wb') as file:
            file.write(image_data)

        # Start the PyTorch operations in a separate thread
        threading.Thread(target=process_image, args=(image_data,)).start()

    # Schedule the fetch_image function to be called again after 5000 milliseconds
    root.after(5000, fetch_image)

# Create the main window
root = tk.Tk()
root.title("BambuHMI Remote Image Viewer (RIV 0.1)")

# Add a label to the window to hold the image
image_label = tk.Label(root)
image_label.pack()

# Add a button to fetch the image
fetch_button = tk.Button(root, text="Fetch Image", command=fetch_image)
fetch_button.pack()

# Start the first image fetch and the Tkinter event loop
fetch_image()  # Start fetching images immediately
root.mainloop()

