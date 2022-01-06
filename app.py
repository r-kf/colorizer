from tkinter import *
import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile, asksaveasfilename
from cv2 import FileNode_NAMED
import os

from numpy.core.fromnumeric import resize

from colorize import colorize

class App:

    def __init__(self, root):

        #setting title
        root.title("colorizer")

        #setting window size
        width=731
        height=501
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        upload_button=tk.Button(root)
        upload_button["bg"] = "#c0c0c0"
        ft = tkFont.Font(family='Arial Bold',size=20)
        upload_button["font"] = ft
        upload_button["fg"] = "#000000"
        upload_button["justify"] = "center"
        upload_button["text"] = "UPLOAD"
        upload_button.place(x=560,y=30,width=130,height=40)
        upload_button["command"] = self.upload

        save_button=tk.Button(root)
        save_button["bg"] = "#c0c0c0"
        ft = tkFont.Font(family='Arial Bold',size=20)
        save_button["font"] = ft
        save_button["fg"] = "#000000"
        save_button["justify"] = "center"
        save_button["text"] = "SAVE"
        save_button.place(x=560,y=130,width=130,height=40)
        save_button["command"] = self.save

        generate_button=tk.Button(root)
        generate_button["bg"] = "#c0c0c0"
        ft = tkFont.Font(family='Arial Bold',size=20)
        generate_button["font"] = ft
        generate_button["fg"] = "#000000"
        generate_button["justify"] = "center"
        generate_button["text"] = "GENERATE"
        generate_button.place(x=560,y=80,width=130,height=40)
        generate_button["command"] = self.generate

        img_input = ImageTk.PhotoImage(Image.open("resources/input_icon.png").resize((343, 285)))
        input_label = Label(root, image=img_input, bg="white")
        input_label.image = img_input
        input_label.place(x=10,y=190,width=343,height=285)

        img_output = ImageTk.PhotoImage(Image.open("resources/output_icon.png").resize((343, 285)))
        output_label = Label(root, image=img_output, bg="white")
        output_label.image = img_output
        output_label.place(x=370,y=190,width=343,height=285)

 
        logo = ImageTk.PhotoImage(Image.open("resources/colorizer.png"))
        GLabel_990=tk.Label(root, image=logo)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_990["font"] = ft
        GLabel_990["fg"] = "#333333"
        GLabel_990["justify"] = "center"
        GLabel_990.image = logo
        GLabel_990["text"] = "LOGO LABEL"
        GLabel_990.place(x=10,y=30,width=425,height=114)

        

    def upload(self):
        self.filename = filedialog.askopenfilename()
        print(self.filename)

        img = ImageTk.PhotoImage(Image.open(self.filename).resize((343, 285))) # !! fix later with own resize method
        
        input_label = Label(image=img, bg="white")
        input_label.image = img
        input_label.place(x=10,y=190,width=343,height=285)


    def save(self):
        print("command")
        
        img = self.generate()

        imgpil = ImageTk.getimage(img)
        if imgpil.mode != "RGB":
            imgpil = imgpil.convert("RGB")
            
        imgpil.save(os.path.join("/examples", asksaveasfilename(initialdir = "/", filetypes = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png')))), "JPEG" )



    def generate(self):
        print("hmmm" + self.filename)

        images = colorize(self.filename)
        colorized = images[1]

        img =  ImageTk.PhotoImage(image=Image.fromarray(colorized).resize((343, 285)))
        
        output_label = Label(image=img, bg="white")
        output_label.image = img
        output_label.place(x=370,y=190,width=343,height=285)

        return img




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()