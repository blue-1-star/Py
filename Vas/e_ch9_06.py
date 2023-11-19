"""
у объекта должно быть поле-список, значением которому можно присваивать только
список. Из присваиваемого списка в поле-список копируются только
текстовые значения. При считывании значения этого поля возвращается 
текстовая строка, содержащая только начальные буквы текстовых
значений, которые входят в список.
"""
class e_ch9_06:
    def __init__(self, li):
        # self.li=[]
        if not isinstance(li, list):            
            raise TypeError("Поле 'li' должно быть списком.")
        # for s in li:
        #     if isinstance(s, str): 
        #         # ls.append(s)
        #         self.li.append(s)
        self.li = [s for s in li if isinstance(s, str)]
    def __str__(self):
        # return str(self.li)
        # os = [s[0]  for s in self.li ] 
        return str([s[0]  for s in self.li ])
A1 = e_ch9_06([1,"4","bnb","True",17,("a",4),"Ua","1a"])
print(A1)
