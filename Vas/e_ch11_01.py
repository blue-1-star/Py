"""
отображается окно с кнопкой, изображением и текстовой меткой. При нажатии кнопки окно закрывается.
"""
from tkinter import *
wnd=Tk()
wnd.title("Simple window with button")
wnd.geometry("900x900")
W, H = 900,900
# example from 552.py
path="G:\\Programming\\Py\\Vas\\picture\\"  
# cats_embrace_01.png  600x659,  Born_Wild_01.png 322x700
# files=["cats_embrace_01.png","tiger1.png","Born_Wild_01.png"]  
files=["cats_embrace_01.png"]
imgs=[PhotoImage(file=path+f) for f in files]
lbl_i=Label(wnd, image=imgs[0])
lbl_i.place(x=150,y=100)
lbl_txt ="my gentle and tender beast"
lbl = Label(wnd,text=lbl_txt,font=("Arial Bold",20))
btn = Button(wnd,text="Close",command=wnd.destroy)
btn.place(x=W/2-20,y=810,width=100,height=40)
lbl.place(x=155,y=760)
wnd.mainloop()
