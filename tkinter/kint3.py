import tkinter as tk

def change_text():
    # This function runs when the button is clicked
    my_label.config(text="You clicked the button!", fg="green")

root = tk.Tk()
root.geometry("500x700")

my_label = tk.Label(root, text="Waiting for click...", font=("Arial", 14))
my_label.pack(pady=20)

# The 'command' parameter links the button to the function
# Note: Do not put parentheses after the function name here!
action_button = tk.Button(root, text="Click Here", command=change_text)
action_button.pack()

root.mainloop()
