###############Functions#############

import constants
import tkinter as tk
import tkinter.filedialog 
from assembler import Assembler
import utils

i = 0

def select_file():
    filepath = tkinter.filedialog.askopenfilename(initialdir=r"D:\Uni\Term 6\System Programming\Project Files\Version 1.2",
                                          title="Select File",
                                          filetypes= (("text files","*.txt"),
                                          ("all files","*.*")))
    
    constants.DEFAULT_PATHS["original_file_path"] = filepath
    global i
    i = 0


def check_intermediate(assembler):
        
        try:
            utils.check_format(assembler.source_file)
        except:
            tk.messagebox.showerror("Error", "Error in input file format. Please try again")
            i = 0
            return

        try:
            assembler.assemble()
            tk.messagebox.showinfo("Sucess!", "Program assembled sucessfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error during assembly: {str(e)}")

        text_1.delete('1.0', tk.END)
        with open(constants.DEFAULT_PATHS["intermediate_file_path"], 'r') as file:
            file_content = file.readlines()
            for line in file_content:
                text_1.insert("end", line)


def pass1_output(assembler):
    text_1.delete('1.0', tk.END)

    text_1.insert("end","Pass 1 Location Counter:\n\n")
    with open(constants.DEFAULT_PATHS["pass1_file_path"], 'r') as file:
            file_content = file.readlines()
            cnt = 0
            for line in file_content:
                if(cnt == 0):
                    line = line.replace('\t', '\t\t', 1)
                    cnt+=1
                text_1.insert("end", line)

    
    text_1.insert("end","\n\nSymbol Table:\n")
    with open(constants.DEFAULT_PATHS["symbol_file_path"], 'r') as file:
        file_content = file.readlines()
        for line in file_content:
            text_1.insert("end", line)        

    text_1.insert("end","\n\nLiteral Table:\n")
    with open(constants.DEFAULT_PATHS["literal_file_path"], 'r') as file:
        file_content = file.readlines()
        for line in file_content:
            text_1.insert("end", line)   
    
def pass2_output(assembler):
    text_1.delete('1.0', tk.END)
    with open(constants.DEFAULT_PATHS["object_code_file_path"], 'r') as file:
            file_content = file.readlines()
            cnt = 0
            for line in file_content:
                if(cnt == 0):
                    idx = line.rfind('\t')
                    line = line[:idx] + '\t' + line[idx:]
                    line = line.replace('\t', '\t\t', 1)
                    cnt+=1
                text_1.insert("end", line)

def htme_output():
    text_1.delete('1.0', tk.END)
    with open(constants.DEFAULT_PATHS["HTME_file_path"], 'r') as file:
            file_content = file.readlines()
            cnt = 0
            for line in file_content:
                text_1.insert("end", line)

def next_button():
    
    assembler = Assembler()
    global i

    if(i == 0):
        check_intermediate(assembler)
        i+= 1

    elif(i == 1):
        pass1_output(assembler)
        i+=1
    elif(i == 2):
        pass2_output(assembler)
        i+=1
    elif(i == 3):
        htme_output()
        i = 0

####################################

from pathlib import Path

from tkinter import *
from tkinter import Tk, Canvas, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Uni\Term 6\System Programming\GUI Build\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("600x450")
window.title("SIC-XE Assembler")
window.configure(bg = "#F6F1DE")


canvas = Canvas(
    window,
    bg = "#F6F1DE",
    height = 450,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    600.0,
    75.0,
    fill="#063970",
    outline="")

canvas.create_text(
    133.0,
    16.0,
    anchor="nw",
    text="SIC - XE Assembler",
    fill="#FFFFFF",
    font=("Itim Regular", 36 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=next_button,
    relief="flat"
)
button_1.place(
    x=364.0,
    y=375.0,
    width=147.0,
    height=49.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=select_file,
    relief="flat"
)
button_2.place(
    x=92.0,
    y=375.0,
    width=147.0,
    height=49.0
)


text_1 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
text_1.place(
    x=21.0,
    y=91.0,
    width=560.0,
    height=267.0
)
window.resizable(False, False)
window.mainloop()