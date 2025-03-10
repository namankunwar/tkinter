from tkinter import *
from PIL import ImageTk, Image

# Initialize the application
root = Tk()
root.title("Image Viewer")
root.geometry("800x600")  # Default window size

# Function to resize the image to fit the current window size
def resize_image(image, width, height):
    return image.resize((width, height), Image.Resampling.LANCZOS)

# Load images
original_images = [
    Image.open("images/saitama.jpg"),
    Image.open("images/ichigo.jpg"),
    Image.open("images/itachi.png"),
    Image.open("images/saitama1.png"),
    Image.open("images/ranpo.png"),
    Image.open("images/noragami.jpg"),
    Image.open("images/gintama.png"),
]

# Store resized images
resized_images = [None] * len(original_images)

# Variables to track the current image and zoom level
current_image = 0
zoom_level = 1.0  # Default zoom level

# Function to update the displayed image dynamically
def update_image(label, index):
    global resized_images, zoom_level
    width = int(root.winfo_width() * zoom_level)
    height = int((root.winfo_height() - 100) * zoom_level)  # Subtract height for buttons
    resized_images[index] = ImageTk.PhotoImage(resize_image(original_images[index], width, height))
    label.config(image=resized_images[index])

# Function to reset zoom level when switching images
def reset_zoom():
    global zoom_level
    zoom_level = 1.0

# Navigation functions
def forward():
    global current_image
    reset_zoom()
    current_image = (current_image + 1) % len(original_images)
    update_image(my_label, current_image)

def back():
    global current_image
    reset_zoom()
    current_image = (current_image - 1) % len(original_images)
    update_image(my_label, current_image)

# Zoom functions
def zoom_in():
    global zoom_level
    zoom_level += 0.1  # Increase zoom level by 10%
    update_image(my_label, current_image)

def zoom_out():
    global zoom_level
    if zoom_level > 0.1:  # Ensure zoom level doesn't go below 10%
        zoom_level -= 0.1
    update_image(my_label, current_image)

# Display the first image
resized_images[current_image] = ImageTk.PhotoImage(original_images[current_image])
my_label = Label(root, image=resized_images[current_image])
my_label.grid(row=0, column=0, columnspan=5, sticky="nsew")

# Add buttons
button_back = Button(root, text="<<", command=back)
button_forward = Button(root, text=">>", command=forward)
button_quit = Button(root, text="Exit", command=root.quit)
button_zoom_in = Button(root, text="Zoom In", command=zoom_in)
button_zoom_out = Button(root, text="Zoom Out", command=zoom_out)

button_back.grid(row=1, column=0, sticky="ew")
button_zoom_out.grid(row=1, column=1, sticky="ew")
button_quit.grid(row=1, column=2, sticky="ew")
button_zoom_in.grid(row=1, column=3, sticky="ew")
button_forward.grid(row=1, column=4, sticky="ew")

# Configure grid for responsiveness
root.grid_rowconfigure(0, weight=1)  # Make row 0 (image row) grow
root.grid_columnconfigure(0, weight=1)  # Make all columns stretch
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# Bind window resize event to dynamically resize images
def resize_event(event):
    update_image(my_label, current_image)

root.bind("<Configure>", resize_event)

# Run the application
root.mainloop()
