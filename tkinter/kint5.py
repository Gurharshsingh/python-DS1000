import tkinter as tk

def login():
    # A simple function to demonstrate the button working
    username = username_entry.get()
    status_label.config(text=f"Logging in as {username}...", fg="green")

root = tk.Tk()
root.title("Login Form (Grid Example)")
root.geometry("300x200") # Made slightly taller to fit the status label

# Row 0
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10) # padx/pady add space around the widget

username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

# Row 1
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)

password_entry = tk.Entry(root, show="*") # Hide password characters
password_entry.grid(row=1, column=1)

# Row 2
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=1, pady=10, sticky="we") # 'sticky' stretches the button

# Row 3 (Status output)
status_label = tk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
