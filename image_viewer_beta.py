from tkinter import *
from tkinter.filedialog import askopenfilenames
from PIL import ImageTk, Image

# Initialize the application
root = Tk()
root.title("Image Annotator and Viewer")
root.geometry("800x600")

# Function to resize the image
def resize_image(image, width, height):
    return image.resize((width, height), Image.Resampling.LANCZOS)

# Store loaded images
original_images = []
resized_images = []
annotations = []  # Store bounding boxes as (x1, y1, x2, y2)

# Variables to track the current image, zoom level, and panning
current_image = 0
zoom_level = 1.0
start_x = 0
start_y = 0
canvas_offset_x = 0
canvas_offset_y = 0
rectangle = None  # To store the current drawing box
annotation_mode = False  # Toggle for annotation mode

# Canvas for displaying images
canvas = Canvas(root, bg="black")
canvas.grid(row=0, column=0, columnspan=5, sticky="nsew")

# Store canvas image ID
canvas_image = None

# Function to update the displayed image
def update_canvas_image():
    global canvas_image, canvas_offset_x, canvas_offset_y, zoom_level, root
    if not original_images:
        return
    
    width = int(original_images[current_image].width * zoom_level)
    height = int(original_images[current_image].height * zoom_level)

    resized_image = resize_image(original_images[current_image], width, height)
    tk_image = ImageTk.PhotoImage(resized_image)
    
    # Remove the previous image
    if canvas_image:
        canvas.delete(canvas_image)

    # Create new image on canvas
    canvas_image = canvas.create_image(canvas_offset_x, canvas_offset_y, image=tk_image, anchor="center")
    canvas.image = tk_image  # Prevent garbage collection

    # Draw the bounding boxes on the resized image
    for bbox in annotations:
        x1, y1, x2, y2 = bbox
        x1_resized = x1 * zoom_level
        y1_resized = y1 * zoom_level
        x2_resized = x2 * zoom_level
        y2_resized = y2 * zoom_level
        canvas.create_rectangle(x1_resized, y1_resized, x2_resized, y2_resized, outline="red", width=2)

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

# Zoom with mouse scroll
def zoom(event):
    global zoom_level
    if event.delta > 0:  # Scroll up
        zoom_level += 0.1
    else:  # Scroll down
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

# Annotation (drawing a rectangle)
def start_annotation(event):
    global start_x, start_y, rectangle
    if annotation_mode:
        start_x = event.x
        start_y = event.y
        # Start drawing a rectangle
        rectangle = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="blue", width=2)

def update_annotation(event):
    global rectangle
    if annotation_mode:
        # Update the rectangle size while dragging the mouse
        canvas.coords(rectangle, start_x, start_y, event.x, event.y)

def save_annotation(event):
    global annotations, start_x, start_y, rectangle
    if annotation_mode:
        # Save the coordinates of the bounding box (before and after dragging)
        x1, y1 = start_x, start_y
        x2, y2 = event.x, event.y
        annotations.append((x1, y1, x2, y2))  # Store as (x1, y1, x2, y2)
        # Clear current drawing
        canvas.delete(rectangle)
        rectangle = None
        update_canvas_image()  # Update the image to show new annotations

# Toggle annotation mode
def toggle_annotation_mode():
    global annotation_mode
    annotation_mode = not annotation_mode
    if annotation_mode:
        status_label.config(text="Annotation Mode: ON")
    else:
        status_label.config(text="Annotation Mode: OFF")

# Function to load multiple images at once
def load_images():
    global original_images, resized_images, annotations, current_image
    file_paths = askopenfilenames(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    original_images = [Image.open(file) for file in file_paths]
    resized_images = [None] * len(original_images)
    annotations = []  # Reset annotations
    current_image = 0  # Reset to the first image
    reset_zoom()  # Reset zoom
    update_canvas_image()

# Delete an annotation when clicked
def delete_annotation(event):
    global annotations
    if not annotation_mode:
        return
    
    # Check if the click is within any annotation box
    for bbox in annotations:
        x1, y1, x2, y2 = bbox
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            annotations.remove(bbox)  # Remove the annotation
            update_canvas_image()  # Redraw the image after deletion
            break

# Add buttons
button_back = Button(root, text="<<", command=back)
button_forward = Button(root, text=">>", command=forward)
button_load = Button(root, text="Load Images", command=load_images)
button_annotation_mode = Button(root, text="Enter Annotation Mode", command=toggle_annotation_mode)
button_quit = Button(root, text="Exit", command=root.quit)

button_back.grid(row=1, column=0, sticky="ew")
button_load.grid(row=1, column=1, sticky="ew")
button_annotation_mode.grid(row=1, column=2, sticky="ew")
button_quit.grid(row=1, column=3, sticky="ew")
button_forward.grid(row=1, column=4, sticky="ew")

# Status label to show annotation mode status
status_label = Label(root, text="Annotation Mode: OFF")
status_label.grid(row=2, column=0, columnspan=5, sticky="ew")

# Configure grid for responsiveness
root.grid_rowconfigure(0, weight=1)  # Make row 0 (image row) grow
root.grid_columnconfigure(0, weight=1)  # Make all columns stretch
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# Bind mouse events for dragging and resizing
canvas.bind("<ButtonPress-1>", start_drag)  # Left mouse button press for dragging
canvas.bind("<B1-Motion>", drag_image)  # Mouse drag (while holding left button)
canvas.bind("<MouseWheel>", zoom)  # Mouse scroll for zooming

# Bind annotation mouse events
canvas.bind("<ButtonPress-3>", start_annotation)  # Right mouse button press for annotation
canvas.bind("<B3-Motion>", update_annotation)  # Right mouse drag to update annotation size
canvas.bind("<ButtonRelease-3>", save_annotation)  # Right mouse button release to save annotation
canvas.bind("<ButtonPress-1>", delete_annotation)  # Left-click to delete annotation if clicked on a box

# Bind window resize event to dynamically resize images
def resize_event(event):
    global canvas_offset_x, canvas_offset_y
    canvas_offset_x = canvas.winfo_width() // 2
    canvas_offset_y = canvas.winfo_height() // 2
    update_canvas_image()

root.bind("<Configure>", resize_event)

# Initial setup
reset_zoom()
update_canvas_image()

# Run the application
root.mainloop()
