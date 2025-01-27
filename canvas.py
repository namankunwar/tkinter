from tkinter import *
from PIL import ImageTk, Image

# Initialize the application
root = Tk()
root.title("Canvas Example")
root.geometry("400x300")

# Create a Canvas widget
canvas = Canvas(root, bg="white", width=400, height=300)
canvas.pack()

# Draw a line on the canvas
canvas.create_line(10, 10, 390, 290, fill="blue", width=2)

# Draw a rectangle on the canvas
canvas.create_rectangle(50, 50, 150, 150, fill="red", outline="black")

# Add text to the canvas
canvas.create_text(200, 100, text="Hello, Canvas!", font=("Arial", 16), fill="green")

# Load an image
image = Image.open("images/ichigo.jpg")
photo = ImageTk.PhotoImage(image)

# Display the image on the canvas
canvas.create_image(200, 150, image=photo)

# Run the application
root.mainloop()