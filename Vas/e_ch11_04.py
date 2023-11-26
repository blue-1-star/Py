"""
отображается окно с двумя кнопками, полем ввода и текстовой меткой.
При вводе текста в текстовое поле он автоматически дублируется в текстовой метке. 
Нажатие одной из кнопок приводит к очистке поля и метки. Нажатие другой кнопки
приводит к закрытию окна.
"""
from tkinter import *
def update_label_text(event):
    text = txt.get()
    lbl.config(text=text)
# def clear_lbl_txt(event):
def clear_lbl_txt():
    lbl.config(text="")
    txt.delete(0,END)
wnd=Tk()
wnd.title("Duplicate text in a label")
W, H = 500, 450
Swh= str(W)+"x"+str(H)
wnd.geometry(Swh)
# lbl_txt =""
txt=Entry(master=wnd, width=50)
txt.pack(pady=10)
lbl = Label(wnd,text="")
lbl.pack(pady=10)
button_frame = Frame(wnd)
button_frame.pack(pady=10)
btn_1=Button(button_frame, text="Clear")
btn_2=Button(button_frame, text="Exit")
btn_1.configure(command=clear_lbl_txt)
btn_2.configure(command=wnd.destroy)
btn_1.pack(side=LEFT,padx=5)
btn_2.pack(side=LEFT,padx=5)
txt.bind("<KeyRelease>",update_label_text)
wnd.mainloop()