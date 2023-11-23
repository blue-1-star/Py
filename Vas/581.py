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
        self.imgFiles=["exit.png","bold.png","italic.png", "normal.png"]
        # path to files directory
        self.path="D:\\Books\\Python\\Pictures\\"
