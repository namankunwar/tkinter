import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Tkinter Example")
root.geometry("300x500")

# Add a label
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 14))
label.pack(pady=20)

# Add a button
def on_click():
    label.config(text="Button Clicked!")

button = tk.Button(root, text="Click Me", command=on_click, fg="red", bg="blue")
button.pack()

# Run the application
root.mainloop()
