from tkinter import *
from PIL import ImageTk, Image

# Initialize the application
root = Tk()
root.title("Image Viewer with Fixed Window Size")
root.geometry("800x600")  # Set fixed window size
root.resizable(False, False)  # Disable window resizing

# Function to resize images to fit the fixed window size
def resize_image(image, width=800, height=500):
    return image.resize((width, height), Image.Resampling.LANCZOS)

# Load and resize images
my_img = ImageTk.PhotoImage(resize_image(Image.open("images/saitama.jpg")))
my_img1 = ImageTk.PhotoImage(resize_image(Image.open("images/ichigo.jpg")))
my_img2 = ImageTk.PhotoImage(resize_image(Image.open("images/itachi.png")))
my_img3 = ImageTk.PhotoImage(resize_image(Image.open("images/saitama1.png")))
my_img4 = ImageTk.PhotoImage(resize_image(Image.open("images/ranpo.png")))
my_img5 = ImageTk.PhotoImage(resize_image(Image.open("images/noragami.jpg")))
my_img6 = ImageTk.PhotoImage(resize_image(Image.open("images/gintama.png")))

# Store images in a list
image_list = [my_img, my_img1, my_img2, my_img3, my_img4, my_img5, my_img6]

# Display the first image
current_image = 0
my_label = Label(image=image_list[current_image])
my_label.grid(row=0, column=0, columnspan=3)

# Navigation functions
def forward(index):
    global current_image, my_label
    current_image = index
    my_label.grid_forget()
    my_label = Label(image=image_list[current_image])
    my_label.grid(row=0, column=0, columnspan=3)

def back(index):
    global current_image, my_label
    current_image = index
    my_label.grid_forget()
    my_label = Label(image=image_list[current_image])
    my_label.grid(row=0, column=0, columnspan=3)

# Add buttons
button_back = Button(root, text="<<", command=lambda: back((current_image - 1) % len(image_list)))
button_forward = Button(root, text=">>", command=lambda: forward((current_image + 1) % len(image_list)))
button_quit = Button(root, text="Exit Program", command=root.quit)

button_back.grid(row=1, column=0)
button_quit.grid(row=1, column=1)
button_forward.grid(row=1, column=2)

# Run the application
root.mainloop()
