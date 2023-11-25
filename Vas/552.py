from tkinter import *
from tkinter.ttk import Combobox
def change(evt):
    t=cb.get()
    for k in range(len(names)):
        if t==names[k]:
            lbl.configure(image=imgs[k])
            break
# path="D:\\Books\\Python\\Pictures\\"
# path="D:\\Programming\\Py\\Vas\\picture\\"        
path="G:\\Programming\\Py\\Vas\\picture\\"        
names=["lion","tiger","cat" ]
# files=["tiger1.jpg","lion.jpg","koala.jpg"]
# cats_embrace_01.png  600x659
files=["cats_embrace_01.png","tiger1.png","Born_Wild_01.png"]
wnd=Tk()
wnd.title("Predators")
wnd.geometry("800x900")
wnd.resizable(False, False)
imgs=[PhotoImage(file=path+f) for f in files]
index=0
lbl=Label(wnd, image=imgs[index])
lbl.configure(relief=GROOVE)
lbl.place(x=10, y=10, width=600, height=659)
cb=Combobox(wnd, state="readonly")
cb.configure(values=names)
cb.current(index)
cb.configure(font=("Arial",11,"bold"))
cb.bind("<<ComboboxSelected>>", change)
cb.place(x=10, y=700, width=200, height=30)
btn=Button(wnd, text="OK")
btn.configure(command=wnd.destroy)
btn.place(x=260, y=700, width=100, height=30)
wnd.mainloop()
