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

# Variables to track the current image, zoom level, and panning
current_image = 0
zoom_level = 1.0
start_x = 0
start_y = 0
canvas_offset_x = 0
canvas_offset_y = 0

# Store loaded images
original_images = []
resized_images = []
annotations = []  # Store bounding boxes as image coordinates (x1, y1, x2, y2)

# Canvas for displaying images
canvas = Canvas(root, bg="black")
canvas.grid(row=0, column=0, columnspan=6, sticky="nsew")

# Store canvas image ID
canvas_image = None
rectangle = None  # To store the current drawing box

# Annotation mode state
annotation_mode = False  # Off by default

# Function to update the displayed image
def update_canvas_image():
    global canvas_image, canvas_offset_x, canvas_offset_y, zoom_level, root
    if not original_images:
        return
    
    # Resize the image based on the current zoom level
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

    # Redraw annotations based on the current zoom level and pan offset
    for bbox in annotations:
        # Convert image coordinates to canvas coordinates
        x1 = bbox["coords"][0] * zoom_level + canvas_offset_x - (original_images[current_image].width * zoom_level) // 2
        y1 = bbox["coords"][1] * zoom_level + canvas_offset_y - (original_images[current_image].height * zoom_level) // 2
        x2 = bbox["coords"][2] * zoom_level + canvas_offset_x - (original_images[current_image].width * zoom_level) // 2
        y2 = bbox["coords"][3] * zoom_level + canvas_offset_y - (original_images[current_image].height * zoom_level) // 2
        # Draw the bounding box
        bbox["id"] = canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=2)

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
    annotations.clear()  # Clear annotations when switching images
    update_canvas_image()

def back():
    global current_image
    reset_zoom()
    current_image = (current_image - 1) % len(original_images)
    annotations.clear()  # Clear annotations when switching images
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
    if not annotation_mode:  # Only allow panning if annotation mode is off
        start_x = event.x
        start_y = event.y

def drag_image(event):
    global start_x, start_y, canvas_offset_x, canvas_offset_y
    if not annotation_mode:  # Only allow panning if annotation mode is off
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
    if annotation_mode:  # Only allow annotation if annotation mode is on
        # Convert canvas coordinates to image coordinates
        start_x = (event.x - canvas_offset_x + (original_images[current_image].width * zoom_level) // 2) / zoom_level
        start_y = (event.y - canvas_offset_y + (original_images[current_image].height * zoom_level) // 2) / zoom_level
        # Start drawing a rectangle
        rectangle = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="blue", width=2)

def update_annotation(event):
    global rectangle
    if annotation_mode and rectangle:  # Only update annotation if annotation mode is on
        # Update the rectangle size while dragging the mouse
        canvas.coords(rectangle, start_x * zoom_level + canvas_offset_x - (original_images[current_image].width * zoom_level) // 2,
                      start_y * zoom_level + canvas_offset_y - (original_images[current_image].height * zoom_level) // 2,
                      event.x, event.y)

def save_annotation(event):
    global annotations, start_x, start_y, rectangle
    if annotation_mode and rectangle:  # Only save annotation if annotation mode is on
        # Convert canvas coordinates to image coordinates
        end_x = (event.x - canvas_offset_x + (original_images[current_image].width * zoom_level) // 2) / zoom_level
        end_y = (event.y - canvas_offset_y + (original_images[current_image].height * zoom_level) // 2) / zoom_level
        # Save the coordinates of the bounding box (before and after dragging)
        annotations.append({"id": rectangle, "coords": (start_x, start_y, end_x, end_y)})  # Store as dictionary
        rectangle = None  # Reset the current drawing box
        update_canvas_image()  # Update the image to show new annotations

# Function to delete a bounding box
def delete_annotation(event):
    if annotation_mode:  # Only allow deletion if annotation mode is on
        # Convert canvas coordinates to image coordinates
        click_x = (event.x - canvas_offset_x + (original_images[current_image].width * zoom_level) // 2) / zoom_level
        click_y = (event.y - canvas_offset_y + (original_images[current_image].height * zoom_level) // 2) / zoom_level
        # Check if the click is inside any bounding box
        for bbox in annotations:
            x1, y1, x2, y2 = bbox["coords"]
            # Check if the click coordinates are within the bounding box
            if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                canvas.delete(bbox["id"])  # Remove the bounding box from the canvas
                annotations.remove(bbox)  # Remove the bounding box from the list
                break

# Function to toggle annotation mode
def toggle_annotation_mode():
    global annotation_mode, button_annotation
    annotation_mode = not annotation_mode  # Toggle the state
    if annotation_mode:
        button_annotation.config(text="Annotation On")
        # Bind annotation events
        canvas.bind("<ButtonPress-1>", start_annotation)  # Left mouse button press for annotation
        canvas.bind("<B1-Motion>", update_annotation)  # Left mouse drag to update annotation size
        canvas.bind("<ButtonRelease-1>", save_annotation)  # Left mouse button release to save annotation
        canvas.bind("<ButtonPress-3>", delete_annotation)  # Right mouse button press to delete annotation
    else:
        button_annotation.config(text="Annotation Off")
        # Unbind annotation events
        canvas.unbind("<ButtonPress-1>")
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<ButtonRelease-1>")
        canvas.unbind("<ButtonPress-3>")
        # Rebind panning events
        canvas.bind("<ButtonPress-1>", start_drag)  # Left mouse button press for panning
        canvas.bind("<B1-Motion>", drag_image)  # Left mouse drag for panning

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

# Add buttons
button_back = Button(root, text="<<", command=back)
button_load = Button(root, text="Load Images", command=load_images)
button_annotation = Button(root, text="Annotation Off", command=toggle_annotation_mode)
button_quit = Button(root, text="Exit", command=root.quit)
button_forward = Button(root, text=">>", command=forward)

button_back.grid(row=1, column=0, sticky="ew")
button_load.grid(row=1, column=1, sticky="ew")
button_annotation.grid(row=1, column=2, sticky="ew")
button_quit.grid(row=1, column=3, sticky="ew")
button_forward.grid(row=1, column=4, sticky="ew")

# Configure grid for responsiveness
root.grid_rowconfigure(0, weight=1)  # Make row 0 (image row) grow
root.grid_columnconfigure(0, weight=1)  # Make all columns stretch
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# Bind mouse events for dragging and resizing
canvas.bind("<ButtonPress-1>", start_drag)  # Left mouse button press for panning
canvas.bind("<B1-Motion>", drag_image)  # Left mouse drag for panning
canvas.bind("<MouseWheel>", zoom)  # Mouse scroll for zooming

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