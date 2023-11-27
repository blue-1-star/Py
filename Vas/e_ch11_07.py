"""
есть группа переключателей, предназначенная для выбора цвета. В окне отображается область,
закрашенная цветом, выбранным в группе переключателей.
"""
from tkinter import *
wnd = Tk()
wnd.title("Radio Button")
fnt_1=["Arial",12,"italic"]
W, H = 600, 600
Swh= str(W)+"x"+str(H)
wnd.geometry(Swh)
def update_color():
    canvas.config(bg=color.get())
frm_rb = Frame(wnd)
color=StringVar()
rb_1 = Radiobutton(frm_rb,text="red", value="red",variable=color,command= update_color)
rb_2 = Radiobutton(frm_rb,text="blue",value="blue",variable=color,command= update_color)
rb_3 = Radiobutton(frm_rb,text="green",value="green", variable=color,command= update_color)
rb_1.pack(side=LEFT)
rb_2.pack(side=LEFT)
rb_3.pack(side=LEFT)
frm_rb.pack(side=BOTTOM)
color.set("blue")
canvas = Canvas(wnd, width=W, height=H)
canvas.pack()
update_color()
wnd.mainloop()

