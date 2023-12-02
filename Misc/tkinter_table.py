from tkinter import *
from tkintertable import TableCanvas, TableModel
import random
from collections import OrderedDict
# tframe = Frame(master)
# tframe.pack()
# table = TableCanvas(tframe)
# table.show()
# table = TableCanvas(frame, model,
#                     cellwidth=60, cellbackgr='#e3f698',
#                     thefont=('Arial',12),rowheight=18, rowheaderwidth=30,
#                     rowselectedcolor='yellow', editable=True)
# data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},
#        'rec2': {'col1': 99.88, 'col2': 321.79, 'label': 'rec3'},
#        'rec3': {'col1': 29.88, 'col2': 408.79, 'label': 'rec2'}
#        }                    
# print(data)
from tkintertable.Testing import sampledata
data=sampledata()
class TestApp(Frame):
    """Basic test frame for the table"""

    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('800x500+200+100')
        self.main.title('Test')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        table = TableCanvas(f, data=data)
        #table.importCSV('test.csv')
        print (table.model.columnNames)
        #table.model.data[1]['a'] = 'XX'
        #table.model.setValueAt('YY',0,2)
        table.show()
        return

app=TestApp()
app.mainloop()       