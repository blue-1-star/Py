from tkinter import *

##def click():
##    msg = Label(window, text = "You pressed the button")
##    msg.place(x = 30, y = 50)
##    button["bg"] = "blue"
##    button["fg"] = "white"
##
##window = Tk()
##window.title("Window Title")
##window.geometry("450x100")
##label = Label(text ="Enter number: ")
##entry_box = Entry( text =0)
##output_box = Message(text=0)
##output_box["bg"] = "red"
##output_box ["fg"] = "white"
##output_box ["relief"] = "sunken"
##list_box = Listbox()
##entry_box ["justify"] = "center"
##button1 = Button(text = "Click here", command = click)
##label.place(x = 50, y = 20, width = 100, height = 25)
##entry_box.delete(0, END)
##num = entry_box.get()
##answer = output_txt["text"]
##output_txt["text"] = total
##window.mainloop()

def Call():
    msg = Label(window, text = "You pressed the button")
    msg.place(x = 30, y = 50)
    button["bg"] = "blue"
    button["fg"] = "white"

def Press():
    msg = Label(window, text="Hello!")
    msg.place(x=30, y = 48)
    

window = Tk()
window.geometry("200x110")
#button = Button(text = "Press me", command = Call)
button = Button(text = "Enter Name", command = Press)
button.place(x = 30, y = 20, width = 120, height = 25)
window.mainloop()
