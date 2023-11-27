"""
есть статический список с названия ми животных. При выборе пункта в статическом списке
в окне отображается изображение выбранного животного.
"""

from tkinter import *
wnd = Tk()
wnd.title("Animal Book")
W, H = 800, 800
Swh= str(W)+"x"+str(H)
wnd.geometry(Swh)

def show_img(event):
    sel_ind = lst.curselection()
    if sel_ind:
        sel_ind=sel_ind[0]
        img_lbl.configure(image=imgs[sel_ind])
def on_enter_pressed(event):
    show_img(event)

files=["cats_embrace_01.png","tiger1.png","Born_Wild_01.png"]  
animals=["cat", "tiger", "pig snout"]
path="G:\\Programming\\Py\\Vas\\picture\\"  
imgs=[PhotoImage(file=path+f) for f in files]
frm_img=Frame(wnd)
frm_lst=Frame(wnd)
img_lbl = Label(frm_img)
img_lbl.pack(side=TOP)
# frm_lst=Frame(wnd,relief="GROOVE")
lst = Listbox(frm_lst, selectmode=SINGLE)
for a in animals:
    lst.insert(END,a)
lst.pack(side=LEFT, padx=6)    
frm_lst.pack(side=BOTTOM)
frm_img.pack(side=TOP) 
lst.bind("<<ListboxSelect>>", show_img)
# lst.bind("<Return>", on_enter_pressed)  # Добавляем обработку клавиши ENTER
lst.bind("<ButtonRelease-1>", on_enter_pressed)  # Изменено на ButtonRelease-1
# wnd.bind("<Return>", on_enter_pressed)  # Заменено на привязку к главному окну
wnd.mainloop()    
