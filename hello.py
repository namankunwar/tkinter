from tkinter import *

root = Tk() # this has to be first in every program
root.title("Tkinter Example")
root.geometry("500x500")

#creating the label widget "text"
mylabel = Label(root, text= "Hello, world !!", font=("Lato", 21))
#mylabel.pack() #shoving it on the screen
mylabel.pack(pady=50)
# Run the application
root.mainloop()