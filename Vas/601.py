# Листинг 11.7. Работа с графикой
from tkinter import *
from math import *
# Function for processing the event related to the cursor hovering over the drawing area
def msEnter(evt):
    # image change
    cnv.itemconfig(Pct, image=img_2)
#  event leave cursor hovering over the drawing area
def msLeave(evt):
    cnv.itemconfig(Pct, image=img_1)
    # deelete old lines near cursor
    cnv.delete("ln")
#  move cursor  over the drawing area
def msMotion(evt):
    x=evt.x
    y=evt.y
    cnv.delete("ln")
    # line display
    cnv.create_line(x,5, x, H-5, fill=clr_C1, width=2, tag="ln")
    cnv.create_line(5, y, W-5, y, fill=clr_C1, width=2, tag="ln")
    # coordinates rectangle
    Rxy=cnv.coords(Rtn)
    # coordinates circle
    Cxy=cnv.coords(Crl)
    # circle centre coordinates
    x0=(Cxy[2]+Cxy[0])/2
    y0=(Cxy[3]+Cxy[1])/2
    # distance from cursor to circle centre
    r=sqrt((x-x0)**2+(y-y0)**2)
    # cursor inside the circle
    if r<R:
        # white fill colour  of the circle
        cnv.itemconfig(Crl, fill=clr_C2)
        # red fill colour  of the rectangle
        cnv.itemconfig(Rtn, fill=clr_C1)
        return
    else:
         # red fill colour  of the circle
        cnv.itemconfig(Crl, fill=clr_C1)
        # cursor inside the rectangle
        if x>Rxy[0] and x<Rxy[2] and y>Rxy[1] and y<Rxy[3]:
            # green fill colour  of the rectangle
            cnv.itemconfig(Rtn, fill=clr_R2)
        # cursor outside the rectangle
        else:
            # white fill colour  of the rectangle
            cnv.itemconfig(Rtn, fill=clr_R1)
    # event button UP
def msUp(evt):
    # group lines move up 1 px    
    cnv.move("Lns",0,-1)
    # circle move down 3 px    
    cnv.move(Crl,0,3)
# Button Down
def msDown(evt):
     # group lines move down 1 px    
    cnv.move("Lns",0, 1)
    # circle move up 3 px    
    cnv.move(Crl,0,-3)
# Button Left
def msLeft(evt):
    # text move 1 px left
    cnv.move(Txt,-1,0)
# Button Right
def msRight(evt):
    # text move 1 px right
    cnv.move(Txt,1,0)
# width and height drawing area
W, H = 600, 400
# width and height rectangle
w, h = 200, 100
# number of lines
N = 10
# decrement for line length 
d = 20
# Radius of circle 
R = 30
# font
fnt=("Arial",20,"bold")
txt = "blue txt"
clr="lightgreen"
# color drawing area
clr_1="lightyellow"
clr_2="yellow"
# colour to paint the circle
clr_C1="red"
clr_C2="white"
# colour to paint the rectangle
clr_R1="white"
clr_R2="green"
wnd=Tk()
wnd.geometry(str(W+10)+"x"+str(H+10)+"+400+300")
wnd.title("Graphics")
wnd.resizable(False, False)
# Creation object for drawing area
cnv=Canvas(wnd, bg=clr_1, bd=3, relief=GROOVE)
# place  drawing area in window
cnv.place(x=5, y=5, width=W, height=H)
cnv.focus_set()
# set focus to drawing area
# Creation text element
Txt=cnv.create_text(W/2,50, text=txt, font=fnt, fill="blue")
# Creation group of horizontal lines
for k in range(N):
    x1=70+k*d
    y1=H/4+10*k
    x2=W-70-d*k
    y2=H/4+10*k
    cnv.create_line(x1, y1, x2, y2, fill=clr, width=5, tag="Lns")
# Coordinates for circle
x1=W/2-R
y1=H/2-R+30
x2=W/2+R
y2=H/2+R+30
# Creation circle
Crl=cnv.create_oval(x1, y1, x2, y2, fill=clr_C1)    
# Coordinates for rectangle
x1=20
y1=H-h-20
x2=x1+w
y2=y1+h
Rtn=cnv.create_rectangle(x1, y1, x2, y2, fill=clr_R1)
img_1=PhotoImage(file="G:\\Programming\\Py\\Vas\\picture\\sad_01.png")
img_2=PhotoImage(file="G:\\Programming\\Py\\Vas\\picture\\smile_01.png")
# Creation object image
Pct=cnv.create_image(W-20, H-20, anchor=SE, image=img_1)
# Handler registration
cnv.bind("<Left>", msLeft)
cnv.bind("<Right>", msRight)
cnv.bind("<Up>", msUp)
cnv.bind("<Down>", msDown)
cnv.bind("<Enter>", msEnter)
cnv.bind("<Leave>", msLeave)
cnv.bind("<Motion>", msMotion)
cnv.bind("<Button-1>", lambda evt: cnv.config(bg=clr_2))
cnv.bind("<Button-3>", lambda evt: cnv.config(bg=clr_1))
wnd.mainloop()


