import tkinter as tk
from tkinter import ttk

def open_toplevel():
    # 3. Toplevel (A new window)
    top = tk.Toplevel(root)
    top.title("Toplevel Window")
    top.geometry("200x150")
    tk.Label(top, text="This is a Toplevel window!").pack(pady=20)

def pri():
    print("option 2 selected")






root = tk.Tk()
root.title("Tkinter Advanced Widgets")
root.geometry("600x600")

# 1. Canvas (For drawing shapes, lines, or adding images)
canvas_label = tk.Label(root, text="1. Canvas (More Shapes & Text):", font=("Arial", 10, "bold"))
canvas_label.pack(anchor="w", padx=10, pady=(10, 0))
canvas = tk.Canvas(root, width=250, height=120, bg="white")
canvas.pack(pady=5)
# # Draw a rectangle and a dashed line
canvas.create_rectangle(10, 10, 80, 80, fill="lightblue")
canvas.create_line(0, 0, 250, 120, fill="red", width=2, dash=(4, 4))
# Draw an oval (circle)
canvas.create_oval(100, 10, 170, 80, fill="lightgreen")
# Draw a polygon (triangle)
canvas.create_polygon(210, 10, 180, 80, 240, 80, fill="pink", outline="black")
# # Add text to the canvas
canvas.create_text(125, 105, text="Canvas Shapes", font=("Arial", 10, "italic"))

# # 2. Text (Multi-line text input)
text_label = tk.Label(root, text="2. Text Widget:", font=("Arial", 10, "bold"))
text_label.pack(anchor="w", padx=10)
text_widget = tk.Text(root, height=4, width=40)
text_widget.pack(pady=5)
text_widget.insert(tk.END, "This is a Text widget.\nYou can type multiple lines here.")

# # 3. Toplevel Button
toplevel_label = tk.Label(root, text="3. Toplevel:", font=("Arial", 10, "bold"))
toplevel_label.pack(anchor="w", padx=10)
btn_toplevel = tk.Button(root, text="Open Toplevel Window", command=open_toplevel)
btn_toplevel.pack(pady=5)

# # 4. Message (For displaying multi-line text, similar to Label but automatically wraps)
message_label = tk.Label(root, text="4. Message:", font=("Arial", 10, "bold"))
message_label.pack(anchor="w", padx=10)
msg = tk.Message(root, text="This is a Message widget. It is great for showing multiple lines of text that automatically wrap based on width.", width=250, bg="lightyellow")
msg.pack(pady=5)

# 5. Menubutton (A drop-down menu button)
menubutton_label = tk.Label(root, text="5. Menubutton:", font=("Arial", 10, "bold"))
menubutton_label.pack(anchor="w", padx=10)
mb = tk.Menubutton(root, text="Options Menu", relief="raised")
mb.menu = tk.Menu(mb, tearoff=0)
mb["menu"] = mb.menu
mb.menu.add_command(label="Option 1", command=lambda: print("Option 1 selected"))
mb.menu.add_command(label="Option 2", command=pri)
mb.pack(pady=5)

# # 6. Progressbar (From tkinter.ttk, shows progress)
progress_label = tk.Label(root, text="6. Progressbar:", font=("Arial", 10, "bold"))
progress_label.pack(anchor="w", padx=10)
progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")
progress.pack(pady=5)

strt = tk.Button(root, text="start", command=progress.start(20))
strt.pack(pady=5)

stop = tk.Button(root, text="stop", command=progress.stop)
stop.pack(pady=5)

# progress["value"] = 50 # Set progress to 50%

# # 7. Spinbox (For selecting from a range of values)
spinbox_label = tk.Label(root, text="7. Spinbox:", font=("Arial", 10, "bold"))
spinbox_label.pack(anchor="w", padx=10)
spinbox = tk.Spinbox(root, from_=0, to=10)
spinbox.pack(pady=5)

root.mainloop()


'''
w
e
n
s
ne
nw
se
sw
'''
