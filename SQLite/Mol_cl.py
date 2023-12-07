import Mol_Mod as mm
from Mol_Mod import f_1_03, f_1_04, f_1_05, f_1_06, f_1_07, f_1_08, f_1_09
class Mol:   
    def set(self,st):
        self.st = st
    def __init__(self,st):
        self.st = st
                # print(self.df)
        if self.st == '1.03':
            f_1_03()
        elif self.st == '1.04':
            f_1_04()
        elif self.st == '1.05':
            f_1_05()
        elif self.st == '1.06':
            f_1_06()
        elif self.st == '1.07':
            f_1_07() 
        elif self.st == '1.08':
            f_1_08()
        elif self.st == '1.09':
            f_1_09()
        else:
            print('Not in range')                   
st='1.09'
mol = Mol(st)
