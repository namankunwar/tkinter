from tkinter import *

root = Tk()
root.title("Simple Calculator")

e = Entry(root, width=32, borderwidth=4)
e.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

# Global variables to store the first number and operation
first_number = None
math_operation = None

# Button functions
def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, current + str(number))

def button_clear():
    e.delete(0, END)

def button_operator(op):
    global first_number, math_operation
    first_number = int(e.get())
    math_operation = op
    e.delete(0, END)

def button_equal():
    second_number = int(e.get())
    e.delete(0, END)
    if math_operation == "+":
        e.insert(0, first_number + second_number)
    elif math_operation == "-":
        e.insert(0, first_number - second_number)
    elif math_operation == "*":
        e.insert(0, first_number * second_number)
    elif math_operation == "/":
        e.insert(0, first_number / second_number)

# Creating buttons
button_1 = Button(root, text="1", command=lambda: button_click(1))
button_2 = Button(root, text="2", command=lambda: button_click(2))
button_3 = Button(root, text="3", command=lambda: button_click(3))
button_4 = Button(root, text="4", command=lambda: button_click(4))
button_5 = Button(root, text="5", command=lambda: button_click(5))
button_6 = Button(root, text="6", command=lambda: button_click(6))
button_7 = Button(root, text="7", command=lambda: button_click(7))
button_8 = Button(root, text="8", command=lambda: button_click(8))
button_9 = Button(root, text="9", command=lambda: button_click(9))
button_0 = Button(root, text="0", command=lambda: button_click(0))

button_addd = Button(root, text="+", command=lambda: button_operator("+"))
button_sub = Button(root, text="-", command=lambda: button_operator("-"))
button_mul = Button(root, text="*", command=lambda: button_operator("*"))
button_div = Button(root, text="/", command=lambda: button_operator("/"))
button_clear = Button(root, text="C", command=button_clear)
button_equal = Button(root, text="=", command=button_equal)

# Placing buttons on the grid
button_1.grid(row=3, column=0, padx=10, pady=10)
button_2.grid(row=3, column=1, padx=10, pady=10)
button_3.grid(row=3, column=2, padx=10, pady=10)
button_4.grid(row=2, column=0, padx=10, pady=10)
button_5.grid(row=2, column=1, padx=10, pady=10)
button_6.grid(row=2, column=2, padx=10, pady=10)
button_7.grid(row=1, column=0, padx=10, pady=10)
button_8.grid(row=1, column=1, padx=10, pady=10)
button_9.grid(row=1, column=2, padx=10, pady=10)
button_0.grid(row=4, column=1, padx=10, pady=10)
button_addd.grid(row=1, column=3, padx=10, pady=10)
button_div.grid(row=2, column=3, padx=10, pady=10)
button_sub.grid(row=3, column=3, padx=10, pady=10)
button_clear.grid(row=4, column=0, padx=10, pady=10)
button_mul.grid(row=4, column=2, padx=10, pady=10)
button_equal.grid(row=4, column=3, padx=10, pady=10)

# Run the application
root.mainloop()
