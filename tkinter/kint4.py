import tkinter as tk

def say_hello():
    # Get the text from the entry widget
    user_name = name_entry.get()
    
    # Update the label with the greeting
    greeting_label.config(text=f"Hello, {user_name}!")
    
    # Clear the entry box
    name_entry.delete(0, tk.END)

root = tk.Tk()
root.geometry("350x250")

# 1. Instruction Label
instruction_label = tk.Label(root, text="Enter your name:")
instruction_label.pack(pady=10)

# 2. Entry Widget (Input box)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# 3. Button to trigger action
greet_button = tk.Button(root, text="Greet Me", command=say_hello)
greet_button.pack(pady=10)

# 4. Label to display the result
greeting_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
greeting_label.pack(pady=20)

root.mainloop()
