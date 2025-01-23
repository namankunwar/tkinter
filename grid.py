from tkinter import *

# Create the main window
root =Tk()
root.title("Tkinter Example")
#root.geometry("300x500")

# Add a label
label = Label(root, text="Hello, Tkinter!", font=("Arial", 14)).grid(row=0, column=0)
label1 = Label(root, text="My name is naman kunwar", font=("Arial", 14)).grid(row=1, column=1)

#label.grid()
#label.grid(row=0, column=0)
#label1.grid(row=0, column=1)
#label1.grid(row=1, column=1)

root.mainloop()