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

# Variables to track the current image, zoom level, and panning
current_image = 0
zoom_level = 1.0  # Default zoom level
start_x = 0
start_y = 0
canvas_offset_x =  0
canvas_offset_y = 0

# Canvas for displaying images
canvas = Canvas(root, bg="black")
canvas.grid(row=0, column=0, columnspan=5, sticky="nsew")


# Store canvas image ID
canvas_image = None

# Function to update the displayed image dynamically
def update_canvas_image():
    global canvas_image, canvas_offset_x, canvas_offset_y, zoom_level, root
    width = int(original_images[current_image].width * zoom_level)
    height = int(original_images[current_image].height * zoom_level)
    resized_image = resize_image(original_images[current_image], width, height)
    tk_image = ImageTk.PhotoImage(resized_image)
    canvas.delete(canvas_image)  # Remove the previous image from the canvas
    canvas_image = canvas.create_image(
        canvas_offset_x, canvas_offset_y, image=tk_image, anchor="center"
    )
    canvas.image = tk_image  # Prevent garbage collection

# Function to reset zoom level and offsets when switching images
def reset_zoom():
    global zoom_level, canvas_offset_x, canvas_offset_y
    zoom_level = 1.0
    canvas_offset_x = canvas.winfo_width() // 2
    canvas_offset_y = canvas.winfo_height() // 2

# Navigation functions
def forward():
    global current_image
    reset_zoom()
    current_image = (current_image + 1) % len(original_images)
    update_canvas_image()

def back():
    global current_image
    reset_zoom()
    current_image = (current_image - 1) % len(original_images)
    update_canvas_image()

# Zoom functions
def zoom_in():
    global zoom_level
    zoom_level += 0.1  # Increase zoom level by 10%
    update_canvas_image()

def zoom_out():
    global zoom_level
    if zoom_level > 0.1:  # Ensure zoom level doesn't go below 10%
        zoom_level -= 0.1
    update_canvas_image()

# Panning functions
def start_drag(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def drag_image(event):
    global start_x, start_y, canvas_offset_x, canvas_offset_y
    dx = event.x - start_x  # Calculate change in X
    dy = event.y - start_y  # Calculate change in Y
    canvas_offset_x += dx
    canvas_offset_y += dy
    update_canvas_image()
    start_x = event.x
    start_y = event.y

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

# Bind mouse events for dragging and resizing
canvas.bind("<ButtonPress-1>", start_drag)  # Left mouse button press
canvas.bind("<B1-Motion>", drag_image)  # Mouse drag (while holding left button)

# Bind window resize event to dynamically resize images
def resize_event(event):
    update_canvas_image()

root.bind("<Configure>", resize_event)

# Initial setup
reset_zoom()
update_canvas_image()

# Run the application
root.mainloop()
