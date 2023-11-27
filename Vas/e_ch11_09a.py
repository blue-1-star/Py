"""
открывается окно с полем ввода
и меткой. В поле вводится выражение (в соответствии с правилами языка Python — 
например, алгебраическое выражение), а в метке отображается значение этого выражения.
Используйте функцию eval() и обработку исключительных ситуаций.
"""
from tkinter import *
def update_label_text(event):
    global error_flag
    try:
        text = txt.get()
        res = eval(text)
        lbl.config(text=res)
        error_flag = False
    except Exception as e:
        lbl.config(text="ERROR")
        error_flag=True
def retry_on_error():
    if error_flag:
        lbl.config(text="")
        error_label.config(text="Please correct the expression")
        txt.delete(0, END)
    else:
        error_label.config(text="")        

wnd=Tk()
wnd.title("calculate expression")
W, H = 500, 450
Swh = f"{W}x{H}"
wnd.geometry(Swh)
txt=Entry(master=wnd, width=60)
txt.pack(pady=10)
lbl = Label(wnd,text="")
lbl.pack(pady=10)
error_label = Label(wnd, text="", fg="red")
error_label.pack(pady=10)
txt.bind("<KeyRelease>",update_label_text)
retry_button = Button(wnd, text="Retry", command=retry_on_error)
retry_button.pack(pady=10)
error_flag = False  
wnd.mainloop()
