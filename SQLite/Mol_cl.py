import Mol_Mod as mm
from Mol_Mod import f_1_03, f_1_04, f_1_05, f_1_06, f_1_07, f_1_08, f_1_09, f_1_10, f_1_11, f_1_12, f_1_13, f_2_01, f_2_02, \
    f_2_03, f_2_04, f_2_05, f_2_06, f_3_01, f_3_02, f_3_03, f_3_04, f_3_05, f_3_06, f_3_07, f_3_08, f_3_09, f_3_10, f_3_11
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
        elif self.st == '1.10':
            f_1_10()    
        elif self.st == '1.11':
            f_1_11()
        elif self.st == '1.12':
            f_1_12()   
        elif self.st == '1.13':
            f_1_13()
        elif self.st == '2.01':
            f_2_01()
        elif self.st == '2.02':
            f_2_02()
        elif self.st == '2.03':
            f_2_03()
        elif self.st == '2.04':
            f_2_04()
        elif self.st == '2.05':
            f_2_05()
        elif self.st == '2.06':
            f_2_06()
        elif self.st == '3.01':
            f_3_01()    
        elif self.st == '3.02':
            f_3_02()                
        elif self.st == '3.03':
            f_3_03()           
        elif self.st == '3.04':
            f_3_04()
        elif self.st == '3.05':
            f_3_05()
        elif self.st == '3.06':
            f_3_06()
        elif self.st == '3.07':
            f_3_07()                 
        elif self.st == '3.08':
            f_3_08()
        elif self.st == '3.09':
            f_3_09()
        elif self.st == '3.10':
            f_3_10()
        elif self.st == '3.11':
            f_3_11() 
        else:
            print('Not in range')                   
st='3.11'
mol = Mol(st)
#st='1.12'
# mol = Mol(st)
