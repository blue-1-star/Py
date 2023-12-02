from tkinter import * 
root = Tk()

row = 5
col = 5
cells = {}
for i in range(row):
    for j in range(col):
        root.columnconfigure(j,weight=20) # making the columns responsive 
        root.rowconfigure(i,weight=20) # making the rows responsive 
        b = Entry(root,text="")
        b.grid(row=i,column=j,sticky=NSEW)
        cells[(i,j)] = b
root.mainloop()