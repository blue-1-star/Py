# Листинг 11.5. Определение параметров шрифта
from tkinter import *
# function to define font characteristics
def getFont():
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
def setAll(*args):
    fnt=getFont()
    lbl.configure(font=fnt)
    lbl.configure(fg=color.get())
    txt = "\nfont "    
    txt+=fnt[0]
    txt+=" size "+str(fnt[1])+"\n"
    if "bold" in fnt:
        txt +=" bold"
    if "italic" in fnt:
        txt +=" italic"        
    if color.get()=="red":
        txt +=" red"
    elif color.get()=="blue":
        txt +=" blue"
    else:         
        txt +=" black"
    txt+=" color\n"
    text.set(txt)
fnt_1=["Arial",12,"italic"]
fnt_2=["Times New Roman",13,"bold","italic"]
# list with font names for static list
fonts=["Times New Roman","Arial","Courier New", "Palatino Linotype","Georgia"]
min_size=15
max_size=21
# width and height of window
W=640
H=420
Hf=140   # height of panel with template text
# width and height of panel with static list 
Wl=W/3
Hl=H-Hf-15
Hb=60 # height of panel with button
# width and height of panel  with slider and switch
Ws=W-Wl-15
Hs=Hl-Hb-5
wnd=Tk()
wnd.title("font options")
wnd.geometry(str(W)+"x"+str(H))
wnd.resizable(False, False)
# panel creation
frm_scale=Frame(wnd, bd=3, relief=GROOVE)
frm_text=Frame(wnd, bd=3, relief=GROOVE)
frm_btn=Frame(wnd, bd=3, relief=GROOVE)
frm_list=Frame(wnd, bd=3, relief=GROOVE)
frm_check=Frame(frm_list, bd=3, relief=GROOVE)
# variables for defining text content in controls
text=StringVar()
color=StringVar()
bold=StringVar()
italic=StringVar()
# text label creation
lbl_text=Label(frm_text, text="sample text:", font=fnt_2)
lbl_color=Label(frm_scale, text="color text:", font=fnt_2)
lbl_size=Label(frm_scale, text="size text:", font=fnt_2)
lbl_font=Label(frm_list, text="name font:", font=fnt_2)
lbl_style=Label(frm_check, text="font style:", font=fnt_2)
# label for displaying the template text
lbl=Label(frm_text, textvariable=text)
lbl.configure(bg="white", relief=RAISED)
# switches
rb_1=Radiobutton(frm_scale, text="red", variable=color)
rb_1.configure(value="red", font=fnt_1)
rb_2=Radiobutton(frm_scale, text="blue", variable=color)
rb_2.configure(value="blue", font=fnt_1)
rb_3=Radiobutton(frm_scale, text="black", variable=color)
rb_3.configure(value="black", font=fnt_1)
# switch is set
color.set("blue")
# Slider sreation
scl=Scale(frm_scale, orient=HORIZONTAL)
scl.configure(from_=min_size, to=max_size)
scl.configure(tickinterval=1, resolution=1)
# handler for the event related to slider position change
scl.config(command=setAll)
# creating options and setting their parameters
chb_1=Checkbutton(frm_check, text="bold", variable=bold)
chb_1.configure(onvalue="bold", offvalue="", font=fnt_1)
chb_2=Checkbutton(frm_check, text="italic", variable=italic)
chb_2.configure(onvalue="italic", offvalue="", font=fnt_1)
# initial state of options
bold.set("")
italic.set("italic")
# Creation static list 
lst=Listbox(frm_list, selectmode=SINGLE, font=fnt_1)
# background colour and colour to highlight the item 
lst.configure(bg="gray96", selectbackground="gray")
lst.configure(activestyle="none", height=len(fonts)+1)
# Filling static list with items
for n in fonts:
    lst.insert(END, n)
# by default first item
lst.select_set(0)
# Handler for static list
lst.bind("<<ListboxSelect>>", setAll)
# Creation button
btn=Button(frm_btn, text="OK", font=fnt_2)
# Handler fot button
btn.configure(command=wnd.destroy)
# Placing labels and slider on panels
lbl_text.pack(side="top", fill="x", padx=5, pady=5)
lbl.pack(side="top", fill="both", padx=5, pady=5)
lbl_color.pack(side="top", fill="x", padx=5, pady=5)
scl.pack(side="bottom", fill="x", padx=5, pady=5)
lbl_size.pack(side="bottom", fill="x", padx=5, pady=[25,5])
lbl_font.pack(side="top", fill="x", padx=5, pady=5)
lbl_style.pack(side="top", fill="x", padx=5, pady=5)        
rb_1.pack(side="left", fill="x", padx=5, pady=5)
rb_2.pack(side="left", fill="x", padx=5, pady=5)
rb_3.pack(side="left", fill="x", padx=5, pady=5)
chb_1.pack(side="left", fill="x", padx=5, pady=5)
chb_2.pack(side="left", fill="x", padx=5, pady=5)
lst.pack(side="top", fill="x", padx=5, pady=5)
btn.pack(side="bottom", fill="x", padx=50, pady=10)
frm_text.place(x=5, y=5, width=W-10, height=Hf)
frm_check.pack(side="bottom", fill="both", padx=5, pady=5)
frm_list.place(x=5, y=Hf+10, height=Hl, width=Wl)
frm_scale.place(x=Wl+10, y=Hf+10, width=Ws, height=Hs)
frm_btn.place(x=Wl+10, y=Hf+Hs+15, width=Ws, height=Hb)
setAll()
color.trace("w", setAll)
bold.trace("w", setAll)
italic.trace("w", setAll)
wnd.mainloop()