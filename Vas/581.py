# Листинг 11.6. Работа с меню
from tkinter import *
from tkinter.messagebox import *
class MyApp:
    def __init__(self):
        self.setValues()
        # Creation MainWindow
        self.makeMainWindow()
        # Defining variables for event handling
        self.setVars()
        self.makeMainMenu()
        # toolbar creation
        self.makeToolBar()
        # support panel creation
        self.makeFrame()
        # context menu creation
        self.makePopupMenu()
        # calculation of template text parameters
        self.apply()
        # variable tracking mode
        self.traceVars()
        # main window display
        self.showMainWindow()
    def setValues(self):
        # width and height main windoe
        self.W,self.H = 500, 200        
        # instrument panel height
        self.h=40
        # size main window
        self.position=str(self.W)+"x"+str(self.H)
        # font names
        self.fonts=["Times New Roman","Arial","Courier New"]
        # dict color names
        self.colors={"red":"red","blue":"blue","black":"black"}
        self.style=[["bold","bold"],["italic","italic"]]
        # list files with pictures
        # self.imgFiles=["exit.png","bold.png","italic.png", "normal.png"]
        # size icons exit_01a.png ...   30x30 px
        self.imgFiles=["exit_01a.png","bold_01a.png","italic_01a.png", "normal_01a.png"]
        # path to files directory
        # self.path="D:\\Books\\Python\\Pictures\\"
        self.path="G:\\Programming\\Py\\Vas\\picture\\" 
        # main font
        self.font=("Courier New",10,"bold")
        # Creation Main Window
    def makeMainWindow(self):
        self.wnd=Tk()
        self.wnd.title("Define font")
        self.wnd.geometry(self.position)
        self.wnd.resizable(False, False)
    # Show Main Window
    def showMainWindow(self):
        self.wnd.mainloop()
    # Creation Main Menu
    def makeMainWindow(self):
        self.wnd=Tk()
        self.wnd.title("Define font")
        self.wnd.geometry(self.position)
        self.wnd.resizable(False, False)
    def showMainWindow(self):
        self.wnd.mainloop()  
    # Creation Main Menu            
    def makeMainMenu(self):
        self.menubar=Menu(self.wnd)                      
    # Creation items Main Menu
        self.mFont=Menu(self.wnd, font=self.font, tearoff=0)
        self.mStyle=Menu(self.wnd, font=self.font, tearoff=0)
        self.mColor=Menu(self.wnd, font=self.font, tearoff=0)
        self.mAbout=Menu(self.wnd, font=self.font, tearoff=0)            
    # Fill menu items
        self.setMenuFont(self.mFont)
        self.setMenuStyle(self.mStyle)
        self.setMenuColor(self.mColor)
        self.mAbout.add_command(label="About program", command=self.showDialog)
        self.mAbout.add_separator()
    # add menu items to panel menu
        self.mAbout.add_command(label="Exit", command=self.clExit)
        self.menubar.add_cascade(label="Font", menu=self.mFont)
        self.menubar.add_cascade(label="Style", menu=self.mStyle)
        self.menubar.add_cascade(label="Color", menu=self.mColor)
        self.menubar.add_cascade(label="Program", menu=self.mAbout)    
        # Setting the main menu for the window
        self.wnd.config(menu=self.menubar)
    def makeToolBar(self):
        # list with names of methods for processing the event related to button pressing
        mt=[self.clExit, self.clBold, self.clItalic, self.clNormal]
        # button panel
        self.toolbar=Frame(self.wnd, bd=3, relief=GROOVE)
        # list for images
        self.imgs=[]
        # list for buttons
        self.btns=[]
        # Creation images and buttons
        for f in self.imgFiles:
            # Creation image
            self.imgs.append(PhotoImage(file=self.path+f))
            # Creation button
            self.btns.append(Button(self.toolbar, image=self.imgs[-1]))
            # Add button to panel
            self.btns[-1].pack(side="left", padx=2, pady=2)
        # define handlers for buttons
        for k in range(len(mt)):
            self.btns[k].configure(command=mt[k])
        # Creation text label
        self.lblSize=Label(self.toolbar, text="Font size:", font=self.font)
        # Place label to panel
        self.lblSize.pack(side="left", padx=2, pady=2)
        # Creation spinner 
        self.spnSize=Spinbox(self.toolbar, from_=15, to=20, font=self.font, width=3, justify="right", \
        textvariable=self.size)
        # place spinner on panel
        self.spnSize.pack(side="left", padx=2, pady=2)
        # place panel to window            
        self.toolbar.place(x=3, y=3, width=self.W-6, height=self.h)                                
    def makeFrame(self):
        # subpanel creation 
        self.frame=Frame(self.wnd, bd=3, relief=GROOVE)
        # creation label and place it to panel
        Label(self.frame, text="Text example:", font=self.font).pack(side="top")
        # creating a label to display the template text
        self.lblText=Label(self.frame, textvariable=self.text, relief=GROOVE, bg="white", height=5)
        # place label to subpanel
        self.lblText.pack(side="top", fill="both", padx=1, pady=1)
        # place subpanel to window
        self.frame.place(x=3, y=self.h+9, width=self.W-6, height=self.H-self.h-12)
    def makePopupMenu(self):
        # creating a context menu object
        self.popup=Menu(self.wnd, tearoff=0, font=self.font)
        # add command to context menu
        self.setMenuFont(self.popup)
        # delimiter addition
        self.popup.add_separator()
        # 
        self.setMenuStyle(self.popup)
        self.popup.add_separator()
        self.setMenuColor(self.popup)
        self.popup.add_separator()
        # define event handler for cintext menu
        self.wnd.bind("<Button-3>", lambda evt: self.popup.tk_popup(evt.x_root, evt.y_root))
        # method for forming menu commands related to font selection
    def setMenuFont(self, menu):
        for f in self.fonts:
            menu.add_radiobutton(label=f, value=f, variable=self.name)
        self.name.set(self.fonts[0])                
    # method for forming menu commands related to style selection
    def setMenuStyle(self, menu):
        for k in range(len(self.style)):
            menu.add_checkbutton(label=self.style[k][1], onvalue=True,offvalue=False, variable=self.bi[k])
        self.bi[0].set(True)
        self.bi[1].set(False)
    # method for forming menu commands related to color selection
    def setMenuColor(self, menu):
        for r in self.colors.keys():
            menu.add_radiobutton(label=self.colors[r], value=r,
            variable=self.color)
        self.color.set("blue")
    # Define font parameters and template text
    def apply(self,*args):
        clr=self.color.get()
        # name font
        nm=self.name.get()
        # size font
        sz=self.size.get()
        # apply colr to label
        self.lblText.configure(fg=clr)
        # list parameters of font
        fnt=[nm, sz]
        # generation of template text and definition of font parameters
        txt=self.colors[clr]+" font "+nm+"\n"
        for k in range(len(self.style)):
            if self.bi[k].get():
                fnt.append(self.style[k][0])
                txt+=self.style[k][1].lower()+" "
            txt+="size "+str(sz)
            # apply font to label
            self.lblText.configure(font=fnt)
            # setting text to label
            self.text.set(txt)
    #   Creation variables for processing events      
    def setVars(self):
        self.text=StringVar()
        self.name=StringVar()
        self.bi=[BooleanVar(), BooleanVar()]
        self.size=IntVar()
        self.color=StringVar()
    # variable value tracking mode
    def traceVars(self):               
        mt=self.apply
        self.name.trace("w", mt)
        self.color.trace("w", mt)
        for k in range(len(self.bi)):
            self.bi[k].trace("w", mt)
        self.size.trace("w", mt)
    def clExit(self):
        self.wnd.destroy()
    def clBold(self):
        self.bi[0].set(not self.bi[0].get())
    def clItalic(self):
        self.bi[1].set(not self.bi[1].get())
    def clNormal(self):
        self.bi[0].set(False)
        self.bi[1].set(False)
    def showDialog(self):
        showinfo("About program", "very simply program")
MyApp()       












