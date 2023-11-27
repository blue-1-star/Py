"""
открывается окно с полем ввода
и меткой. В поле вводится выражение (в соответствии с правилами языка Python — 
например, алгебраическое выражение), а в метке отображается значение этого выражения.
Используйте функцию eval() и обработку исключительных ситуаций.
"""
from tkinter import *
def update_label_text(event):
    try:
        text = txt.get()
        res = eval(text)
        lbl.config(text=res)
    except Exception as e:
        lbl.config(text="ERROR")

wnd=Tk()
wnd.title("calculate expression")
W, H = 500, 450
Swh = f"{W}x{H}"
wnd.geometry(Swh)
txt=Entry(master=wnd, width=60)
txt.pack(pady=10)
lbl = Label(wnd,text="")
lbl.pack(pady=10)
txt.bind("<KeyRelease>",update_label_text)
wnd.mainloop()
