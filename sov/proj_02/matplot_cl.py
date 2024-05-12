import matplot as mp
import seab as sb
from matplot import f_1_03, f_1_04, f_1_05, f_1_06, f_1_07, f_2_4_2, f_3_2_1, f_3_2_1a, f_3_9, f_3_11, f_3_3_1,\
f_3_3_2, f_3_3_3, f_4_1, f_4_2, f_4_3_1, f_4_3_1_1, f_4_3_1_2, f_4_3_2_1, f_4_3_2_2
from seab import f_6_2_1, f_6_2_2, f_6_2_3, f_7_1,  f_7_3_1, f_8_2_1, f_8_2_1a, f_8_3, f_8_5, f_9_2, f_9_3,\
f_9_4_2, f_9_55, f_9_5, f_10_1

class Matplot:   
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
        elif self.st == '2.4.2':
            f_2_4_2()
        elif self.st == '3.2.1':                  
            f_3_2_1()
        elif self.st == '3.2.1a':
            f_3_2_1a()
        elif self.st == '3.9':
            f_3_9()             
        elif self.st == '3.11':
            f_3_11() 
        elif self.st == '3.3.1':
            f_3_3_1()
        elif self.st == '3.3.2':
            f_3_3_2()
        elif self.st == '3.3.3':
            f_3_3_3()            
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
        elif self.st == '3.12':
            f_3_12() 
        elif self.st == '4.05':
            f_4_05()             
        elif self.st == '4.06':
            f_4_06()  
        elif self.st == '4.07':
            f_4_07()                                
        elif self.st == '4.08':
            f_4_08()
        elif self.st == '4.09':
            f_4_09()
        elif self.st == '4.1':
            f_4_1()
        elif self.st == '4.2':
            f_4_2()
        elif self.st == '4.3.1':
            f_4_3_1()
        elif self.st == '4.3.1.1':
            f_4_3_1_1()     
        elif self.st == '4.3.1.2':
            f_4_3_1_2()
        elif self.st == '4.3.2.1':
            f_4_3_2_1()
        elif self.st == '4.3.2.2':
            f_4_3_2_2()                        
        elif self.st == '6.2.1':
            f_6_2_1()        
        elif self.st == '6.2.2':
            f_6_2_2()
        elif self.st == '6.2.3':
            f_6_2_3()
        elif self.st == '7.1':
            f_7_1()
        elif self.st == '7.3.1':
            f_7_3_1()
        elif self.st == '8.2.1':
            f_8_2_1()
        elif self.st == '8.2.1a':
            f_8_2_1a()
        elif self.st == '8.3':
            f_8_3()
        elif self.st == '8.5':
            f_8_5()
        elif self.st == '9.2':
            f_9_2()
        elif self.st == '9.3':
            f_9_3()
        elif self.st == '9.4.2':
            f_9_4_2()
        elif self.st == '9.55':
            f_9_55()
        elif self.st == '9.5':
            f_9_5()
        elif self.st == '10.1':
            f_10_1()
        else:
            print('Not in range')                   
st='10.1'
# st='9.55'
Matplot(st)
