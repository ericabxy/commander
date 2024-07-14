import tkinter as tk

def on_button_toggle():
    if var.get() == 1:
        print("Checkbutton is selected")
    else:
        print("Checkbutton is deselected")

root = tk.Tk()

# Creating a Checkbutton
var = tk.IntVar()
checkbutton = tk.Checkbutton(root, text="Enable Feature", variable=var, 
                             onvalue=1, offvalue=0, command=on_button_toggle)

# Placing the Checkbutton in the window
checkbutton.pack(padx=40, pady=40)

# Calling methods on the Checkbutton
checkbutton.flash()

root.mainloop()
