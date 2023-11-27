from tkinter import *
wnd = Tk()
wnd.title("Animal Book")
fnt_1=["Arial",12,"italic"]
W, H = 800, 800
Swh= str(W)+"x"+str(H)
wnd.geometry(Swh)
animals=["cat", "tiger", "pig snout"]
frm_lst=Frame(wnd, bd=3,relief=GROOVE)
# frm_lst=Frame(wnd)
lst = Listbox(frm_lst, selectmode=SINGLE)
lst.pack(side=LEFT, padx=5, pady= 5) 
# lst = Listbox(frm_lst, selectmode=SINGLE,font=fnt_1)
lst.configure(bg="gray96", selectbackground="gray")
# lst.configure(activestyle="none", height=len(animals))
lst.configure(height=len(animals))
for a in animals:
    lst.insert(END,a)
    # print("add animal:", a)
# lst.select_set(0)
# frm_lst.place(x=10, y=10)  #  !!! 
frm_lst.pack(side=BOTTOM) 
wnd.mainloop()    
