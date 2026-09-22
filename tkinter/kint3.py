import tkinter as tk

def change_text():
    # This function runs when the button is clicked
    label.config(text="You clicked the button!", fg="green")

root = tk.Tk()
root.geometry("500x700")

label = tk.Label(root, text="Click to change Text", font=("Arial", 14))
label.pack(pady=20)

# The 'command' parameter links the button to the function
# Note: Do not put parentheses after the function name here!
button = tk.Button(root, text="Click Here", command=change_text)
button.pack()

root.mainloop()
