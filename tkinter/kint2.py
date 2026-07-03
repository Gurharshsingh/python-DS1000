import tkinter as tk

root = tk.Tk()
root.title("Widgets Example")
root.geometry("300x200")

# Create a Label widget
my_label = tk.Label(root, text="Hello, Tkinter!", font=("Helvetica", 16))
# Put it on the screen
my_label.pack() # pady adds some vertical padding

# Create a Button widget
my_button = tk.Button(root, text="Click Me!", bg="blue", fg="white")
my_button.pack()

root.mainloop()
