"""
отображается окно с областью для рисования. В центре области находится окружность.
При нажатии кнопок «вверх», «вниз», «влево» или «вправо» окружность начинает дви-
гаться к одному из углов области рисования.
"""
from tkinter import *
def msDown(evt):
    cnv.move(Crl,0,3)
def msUp(evt):
    cnv.move(Crl,0,-3)
def msLeft(evt):
    cnv.move(Crl,-3,0)    
def msRight(evt):
    cnv.move(Crl,+3,0)    
wnd = Tk()
wnd.title("Motion Circle")
clr_C1="lightgreen"
clr_1="lightyellow"
W, H = 800, 600
Swh = f"{W}x{H}"
wnd.geometry(Swh)
# cnv=Canvas(wnd,width=W,height=H)
R=30
x1=W/2-R
y1=H/2-R+30
x2=W/2+R
y2=H/2+R+30
cnv=Canvas(wnd, bg=clr_1, bd=3, relief=GROOVE, width=W,height=H)
Crl=cnv.create_oval(x1, y1, x2, y2, fill=clr_C1)
# cnv.place(x=5, y=5)
cnv.pack(side=BOTTOM)
wnd.bind("<Up>", msUp)
wnd.bind("<Down>", msDown)
wnd.bind("<Left>", msLeft)
wnd.bind("<Right>", msRight)
wnd.mainloop()
