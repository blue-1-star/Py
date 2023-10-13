#import random
from tkinter import *

def sum():  
    num = textbox1.get()
    Sm = textbox2["text"]
    Sm = int(Sm)
    Sm = Sm + int(num) 
    textbox2["text"] = Sm
    textbox1.delete(0,END)

    #message = str(num)
    textbox2["bg"] = "yellow"
    textbox2["fg"] = "blue"
    
def clear():
    Sm=0
    textbox2["text"] = 0
    textbox1.delete(0, END)
    textbox1.focus()

num =0 
Sm = 0

window = Tk()
window.geometry("500x200")
label1 = Label(text = "Enter number: ")
label1.place(x = 50, y = 20, width = 100, height = 25)
textbox1 = Entry(text = 0)
textbox1.place(x = 150, y = 20, width = 100, height = 25)
textbox1["justify"] = "center"
textbox1.focus()
label2 = Label(text = "Sum = ")
label2.place(x=50, y = 50, width = 100, height = 25)

button1 = Button(text = "Sum", command = sum)
button1.place(x = 30, y = 50, width = 40, height = 25)
textbox2 = Message(text = 0)
textbox2.place(x = 150, y = 50, width = 100, height = 25)
textbox2["bg"] = "white"
textbox2["relief"] = "sunken"

button2 = Button(text = "Clear", command = clear)
button2.place(x = 300, y = 50, width = 50, height = 25)

window.mainloop()
