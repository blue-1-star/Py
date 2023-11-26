"""
отображается окно с шаблонным текстом. Окно содержит две кнопки. 
При нажатии одной кнопки размер шрифта (которым отображается шаблонный текст) увеличивается
на единицу. При нажатии другой кнопки размер шрифта уменьшается на единицу.
https://tkdocs.com/tutorial/fonts.html
Fonts, Colors, Images
"""
from tkinter import *
lbl_txt="Template text in label"
f1 = ["Arial",14,"bold"]
# Невинная задача - не имея никаких параметров шрифта просто увеличить его размер
# оставляя все остальные как есть в исходном образце
# с применением все мощи GPT - не получилось 
# для приближения взял функцию getFont  Васильев с 560
# по умолчанию Current font:  TkDefaultFont  и в него не дает доступиться для получения параметров
def getFont():    # 
    res=[]
    # font name
    name=lst.get(lst.curselection())
    # font size
    size=scl.get()    # 
    # add items to the list
    res.append(name)
    res.append(size)
    # if the bold style option is set
    if bold.get()!="":
        res.append(bold.get())
    # if the italic style option is set    
    if italic.get()!="":
        res.append(italic.get())        
    return res
def increase(lbl):
    cf = lbl.cget("font").split()   # cget() return string text parameters - split create list 

    # Получаем размер шрифта и увеличиваем
    new_size=int(cf[1])+1
    new_font = cf[:1]+[new_size]+cf[2:]  # change new_size font 
    # Устанавливаем новый шрифт для метки
    lbl.config(font=new_font)
def decrease(lbl):
    cf = lbl.cget("font").split()   # cget() return string text parameters - split create list 
    # Получаем размер шрифта и увеличиваем
    new_size=int(cf[1])-1
    new_font = cf[:1]+[new_size]+cf[2:]  # change new_size font 
    # Устанавливаем новый шрифт для метки
    lbl.config(font=new_font)
def get_fnt(lbl):
    # current_font = lbl.cget("font")
    cf = lbl.cget("font")
    print("type:",type(cf))
    fc=cf.split()
    print(type(fc)," ",len(fc), type(fc[1]), " ",fc[1], "weight=",fc[2])
    new_size=int(cf.split()[1])+1
    print("size cf[1]=",cf.split()[1],"new size=",new_size)
    # sz = str(cf[1]+1)
    # c_sz= int(cf[1])
    # print("Current font: ",cf,"size=",c_sz)
    print("Current font: ",cf," size=")
    # sz= int(cf[1])+1 
    # nf= cf[:1]+(sz,)+cf[2:]
    # print(cf)
    # print(nf)
wnd=Tk()
wnd.title("Increase - decrease text size by click on button")
W, H = 500, 450
Swh= str(W)+"x"+str(H)
wnd.geometry(Swh)
# lbl_txt =""
lbl = Label(wnd,text=lbl_txt, font=f1)
# current_font = lbl.cget("font")  # Получаем текущий шрифт
lbl.pack(pady=10)
button_frame = Frame(wnd)
button_frame.pack(pady=10)
btn_1=Button(button_frame, text="+")
btn_2=Button(button_frame, text="-")
btn_1.configure(command=lambda: increase(lbl))
btn_2.configure(command=lambda: decrease(lbl))
btn_1.pack(side=LEFT,padx=5)
btn_2.pack(side=LEFT,padx=5)
# get_fnt(lbl)
# btn_2.configure(command=wnd.destroy)
# lbl.bind("<KeyRelease>",update_label_text)
wnd.mainloop()