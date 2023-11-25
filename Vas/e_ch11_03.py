"""
отображается окно с полем ввода, в которое следует ввести возраст пользователя. Программа должна
по возрасту (и текущему году) вычислить год рождения, который отображается в следующем диалоговом окне.
"""
from tkinter import *
from datetime import datetime
def clicked():
    global t
    t=txt.get()
    wnd.destroy()
wnd=Tk()
wnd.title("Your Age")
t=""
W, H = 300, 120
Swh= str(W)+"x"+str(H)
wnd.geometry(Swh)
f1, f2, f3 = ("Arial",13,"bold"),("Arial",13,"italic"),("Arial",10,"bold")
lbl = Label(master=wnd, text="your age?")
lbl.configure(font=f1)
lbl.place(x=10, y=20)
txt=Entry(master=wnd, width=30)
txt.configure(font=f2)
txt.place(x=10, y=50)
btn_1=Button(master=wnd, text="OK")
btn_2=Button(master=wnd, text="Cancel")
btn_1.configure(font=f3)
btn_1.configure(command=clicked)
btn_2.configure(font=f3)
btn_2.configure(command=wnd.destroy)
btn_1.place(x=40, y=80, width=100, height=30)
btn_2.place(x=150, y=80, width=100, height=30)
wnd.mainloop()
def YearBorn(n):
    return datetime.now().year - n
def is_integer(s):
    return s.isdigit()
if is_integer(t):
    msg=Tk()
    msg.title("You was born in " + str(YearBorn(int(t)))) 
    msg.geometry(Swh)
    lbl=Label(master=msg, text="Your Year born is " + str(YearBorn(int(t))), relief=GROOVE)
    lbl.configure(font=f1)
    lbl.place(x=10, y=10, height=40, width=300)
    btn=Button(master=msg, text="OK")
    btn.configure(font=f3)
    btn.configure(command=msg.destroy)
    btn.place(x=110, y=60, width=100, height=30)
    msg.mainloop()



