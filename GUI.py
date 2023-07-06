import cv2
import tensorflow as tf
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Load the trained model
model = tf.keras.models.load_model('child_detection_model.h5')

# Create the GUI window
window = Tk()
window.title("Child Detection")
window.geometry("400x350")

# Function to process and display the selected image
def display_selected_image():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))

    # Read the image using OpenCV
    image = cv2.imread(file_path)

    # Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize the image to fit the GUI window
    image = cv2.resize(image, (300, 250))

    # Convert the image to PIL format
    image = Image.fromarray(image)

    # Create a Tkinter-compatible photo image
    photo = ImageTk.PhotoImage(image)

    # Display the selected image
    image_label.configure(image=photo)
    image_label.image = photo

# Function to detect whether the selected image contains a child or not
def detect_child():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))

    # Read the image using OpenCV
    image = cv2.imread(file_path)

    # Preprocess the image
    image = cv2.resize(image, (100, 100))  # Resize the image to match the input size of the model
    image = image.astype("float") / 255.0  # Normalize the pixel values to the range [0, 1]
    image = tf.expand_dims(image, axis=0)  # Add an extra dimension for batch size

    # Use the trained model to predict the class
    prediction = model.predict(image)

    # Get the predicted class label
    if prediction[0][0] > 0.5:
        label = "Child"
    else:
        label = "Not a child"

    # Display the result
    result_label.configure(text=label)

# Create a button to select and display an image
select_button = Button(window, text="Select Image", command=display_selected_image)
select_button.pack(pady=10)

# Create an image label to display the selected image
image_label = Label(window)
image_label.pack()

# Create a button to detect whether the selected image contains a child or not
detect_button = Button(window, text="Detect Image", command=detect_child)
detect_button.pack(pady=10)

# Create a label to display the result
result_label = Label(window, text="")
result_label.pack()

# Start the GUI main loop
window.mainloop()
