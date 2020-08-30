from tkinter import *
from PIL import Image
from PIL import ImageTk

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

def home_screen():
    global score
    # header_image = canvas.create_image(130, 30, image=tile)
    score_output = "SCORE  " + str(score)
    # score_display = canvas.create_text(550, 25, fill="white", text=score_output, font="Arial 16 bold")
    # for r in range(3):
    #    for c in range(4):
    #       Label(window, text='R%s/C%s'%(r,c),
    #          borderwidth=1 ).grid(row=r,column=c)
    frame = Frame(window)
    frame.grid(row=0,column=0, sticky="n")

    label1=Label(frame, text="Figure").grid(row=0,column=0, sticky="nw")
    label2=Label(frame, text="X").grid(row=1,column=0, sticky="w")
    label3=Label(frame, text="Y").grid(row=2,column=0, sticky="w")
    entry = Entry(frame).grid(row = 1,column = 1,sticky = E+ W)
    entry1 = Entry(frame).grid(row = 2,column = 1, sticky = E)
    Button1=Button(frame,text="Draw").grid(row = 3,column = 1, sticky = "we")
    # figure1=self.canvas.create_rectangle(80, 80, 120, 120, fill="blue")


score = 0
width = 650
height = 600
window = create_window(width, height) # calls the create_window function.
# canvas = Canvas(window, width=width, height=height, bg="white")
# canvas.pack(fill=BOTH, expand=YES)
# canvas.create_rectangle(0, 0, (width), 55, fill="#191618", width=1, outline="black")
window.rowconfigure(10, weight=1)
window.columnconfigure(11, weight=1)
main = Frame(window, bg='black')
main.rowconfigure(7, weight=1)
main.columnconfigure(0, weight=1)
main.grid(row=10, column=0, sticky="news")

# image = Image.open("../../static/graphics/logo_img.jpg")
# image = image.resize((100, 50), Image.ANTIALIAS)
# logo = ImageTk.PhotoImage(image)
lightning = PhotoImage(file="../../static/graphics/lightning.png")
tile = PhotoImage(file="../../static/graphics/tile.png")
tile_locked = PhotoImage(file="../../static/graphics/locked.png")
tile_opened = PhotoImage(file="../../static/graphics/tile-opened.png")
unicorn = PhotoImage(file="../../static/graphics/unicorn.png")


home_screen() # sets up the game environment
window.mainloop()
