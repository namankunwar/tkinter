from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Image Viewer with Navigation")
root.iconbitmap("images/icon.png")

# Load the images
my_img = ImageTk.PhotoImage(Image.open("images/saitama.jpg"))
my_img1 = ImageTk.PhotoImage(Image.open("images/ichigo.jpg"))
my_img2 = ImageTk.PhotoImage(Image.open("images/itachi.png"))
#my_img3 = ImageTk.PhotoImage(Image.open("images/saitama1.png"))
my_img4 = ImageTk.PhotoImage(Image.open("images/ranpo.png"))
my_img5 = ImageTk.PhotoImage(Image.open("images/noragami.jpg"))
my_img6 = ImageTk.PhotoImage(Image.open("images/gintama.png"))

# List of images
image_list = [my_img, my_img1, my_img2,  my_img4, my_img5, my_img6]

# Current image index
current_image = 0

# Display the first image
my_label = Label(image=image_list[current_image])
my_label.grid(row=0, column=0, columnspan=3)

# Navigation functions
def forward(index):
    global current_image, my_label
    current_image = index
    my_label.grid_forget()  # Remove the current image
    my_label = Label(image=image_list[current_image])
    my_label.grid(row=0, column=0, columnspan=3)

def back(index):
    global current_image, my_label
    current_image = index
    my_label.grid_forget()  # Remove the current image
    my_label = Label(image=image_list[current_image])
    my_label.grid(row=0, column=0, columnspan=3)

# Buttons for navigation
button_back = Button(root, text="<<", command=lambda: back((current_image - 1) % len(image_list)))
button_forward = Button(root, text=">>", command=lambda: forward((current_image + 1) % len(image_list)))
button_quit = Button(root, text="Exit Program", command=root.quit)

button_back.grid(row=1, column=0)
button_forward.grid(row=1, column=2)
button_quit.grid(row=1, column=1)

root.mainloop()
