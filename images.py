from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("icons, images, exit")
root.iconbitmap("images\icon.png")
#root.geometry("500x500")

#Loading the image
my_img = ImageTk.PhotoImage(Image.open("images\saitama.jpg"))
my_label = Label(image= my_img) #Labeling the image
my_label.pack()

button_quit = Button(root, text =" Exit the program", command=root.quit)
button_quit.pack()


root.mainloop()