from tkinter import *

# Create the main window
root =Tk()
root.title("Tkinter Example")
root.geometry("300x500")

#input box
e = Entry(root, width=50, bg="grey", borderwidth=4)

e.insert(0,"Enter you name here : ") # act as placeholder with deaful value 0
e.pack()

#define function
def onclick():
    global label1

    txt = e.get()
    new_txt = 'hello' + txt.split(':')[-1]
    label1.config(text=new_txt)

#add button
label1 = Label(root, text= '')

button = Button(root, text="Enter your name!", command=onclick,bg="grey", padx=10, pady=10) #size of button on padx and pady
button.pack(padx=50, pady=100)
#button.grid(row=3, column=3)   
label1.pack()

root.mainloop()