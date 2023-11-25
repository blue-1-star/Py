"""
отображается окно с кнопкой и изображением. При нажатии кнопки окно закрывается.
При наведении курсора на область изображения оно меняется на другое. Когда курсор по-
кидает область изображения, оно меняется на исходное
"""
from tkinter import *
wnd=Tk()
wnd.title("changing the image when hovering the cursor")
wnd.geometry("900x900")
W, H = 900,900
# example from 552.py
path="G:\\Programming\\Py\\Vas\\picture\\"  
# cats_embrace_01.png  600x659,  Born_Wild_01.png 322x700
# files=["cats_embrace_01.png","tiger1.png","Born_Wild_01.png"]  
# files=["cats_embrace_01.png"]
# imgs=[PhotoImage(file=path+f) for f in files]
clr_1="lightyellow"
cnv = Canvas(wnd,bg=clr_1)
img_1=PhotoImage(file="G:\\Programming\\Py\\Vas\\picture\\sad_01.png")
img_2=PhotoImage(file="G:\\Programming\\Py\\Vas\\picture\\smile_01.png")
Pct=cnv.create_image(W/2, H/2, anchor=SE, image=img_1)
# lbl_i=Label(wnd, image=imgs[0])
# lbl_i.place(x=150,y=100)
# lbl_txt ="my gentle and tender beast"
# lbl = Label(wnd,text=lbl_txt,font=("Arial Bold",20))
cnv.place(x=5, y=5, width=W, height=H)
cnv.focus_set()
btn = Button(wnd,text="Close",command=wnd.destroy)
btn.place(x=W/2-20,y=810,width=100,height=40)

# lbl.place(x=155,y=760)
def msEnter(evt):
    # image change
    cnv.itemconfig(Pct, image=img_2)
#  event leave cursor hovering over the drawing area
def msLeave(evt):
    cnv.itemconfig(Pct, image=img_1)
    # deelete old lines near cursor
cnv.bind("<Enter>", msEnter)
cnv.bind("<Leave>", msLeave)    
wnd.mainloop()
