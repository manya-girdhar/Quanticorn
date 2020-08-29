from tkinter import *

def create_window(width_of_window, height_of_window):
    global width_of_screen, height_of_screen, x_position, y_position
    window = Tk()
    window.title("Quanticorn")
    width_of_screen = window.winfo_screenwidth()
    height_of_screen = window.winfo_screenheight()
    x_position = int((width_of_screen/2) - (width_of_window/2))
    y_position = int((height_of_screen/2) - (height_of_window/2))-25  # remove -25
    window.geometry("{}x{}+{}+{}".format(width_of_window, height_of_window,
                                         x_position, y_position))
    window.resizable(False, False)
    return window



width = 650
height = 600
window = create_window(width, height) # calls the create_window function.
canvas = Canvas(window, width=width, height=height, bg="#191618")
canvas.pack(fill=BOTH, expand=YES)
canvas.create_rectangle(0, 0, (width), 50, fill="black", width=1, outline="white")
# start_screen()
window.mainloop()
