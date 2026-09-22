import tkinter as tk

root = tk.Tk()
root.title("Widgets Example")
root.geometry("300x200")

# Create a Label widget
label = tk.Label(root, text="Hello, Tkinter!", font=("Helvetica", 16))
# Put it on the screen
label.pack(pady = 20) # pady adds some vertical padding

# Create a Button widget
button = tk.Button(root, text="Click Me!", bg="blue", fg="white")
button.pack(pady=30)

root.mainloop()
