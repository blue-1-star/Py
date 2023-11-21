from tkinter import *
from tkinter.ttk import Combobox
def change(evt):
    t=cb.get()
    for k in range(len(names)):
        if t==names[k]:
            lbl.configure(image=imgs[k])
            break
# path="D:\\Books\\Python\\Pictures\\"
path="D:\\Programming\\Py\\Vas\\picture\\"        
names=["lion","tiger","cat" ]
# files=["tiger1.jpg","lion.jpg","koala.jpg"]
files=["cats_embrace.png","tiger1.png","Born_Wild.png"]
wnd=Tk()
wnd.title("Predators")
wnd.geometry("660x800")
wnd.resizable(False, False)
imgs=[PhotoImage(file=path+f) for f in files]
index=0
lbl=Label(wnd, image=imgs[index])
lbl.configure(relief=GROOVE)
lbl.place(x=10, y=10, width=500, height=500)
cb=Combobox(wnd, state="readonly")
cb.configure(values=names)
cb.current(index)
cb.configure(font=("Arial",11,"bold"))
cb.bind("<<ComboboxSelected>>", change)
cb.place(x=10, y=220, width=200, height=30)
btn=Button(wnd, text="OK")
btn.configure(command=wnd.destroy)
btn.place(x=60, y=260, width=100, height=30)
wnd.mainloop()
