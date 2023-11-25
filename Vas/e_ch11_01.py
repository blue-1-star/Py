"""
отображается окно с кнопкой, изображением и текстовой меткой. При нажатии кнопки окно закрывается.
"""
from tkinter import *
wnd=Tk()
wnd.title("Simple window with button")
wnd.geometry("550x400")
lbl = Label(wnd,text="Hello!",font=("Arial Bold",20))
btn = Button(wnd,text="Close",command=wnd.destroy)
btn.place(x=40,y=140,width=100,height=40)
lbl.place(x=40,y=30)
wnd.mainloop()
