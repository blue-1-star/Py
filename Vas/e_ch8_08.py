"""
создается цепочка объектов. Для создания цепочки объектов предложите функцию, при вызове которой
в качестве аргумента передается целое число, определяющее количество
объектов в цепочке. Результатом функция должна возвращать ссылку
на первый объект в цепочке.
"""
# class Chain_m:
#     def __init__(self, name, n=1):
#         if n == 1:
#             self.next = None
#         else: 
#             self.next = Chain_m(name,n+1) 
#     def set(self, num=1):
#         self.code=self.name+"["+str(num)+"]"
#         if self.next!=None:
#             self.next.set(num+1) 
#     def show(self):
#         print(self.code)
#         if self.next!=None:
#             self.next.show()

# A = Chain_m("my_chain")
# A.show()
# GPT
class Chain_mg:
    def __init__(self, name, n=1):
        self.name = name
        self.next = None
        if n > 1:
            self.next = Chain_mg(name, n - 1)
            
    def set(self, num=1):
        self.code = self.name + "[" + str(num) + "]"
        if self.next is not None:
            self.next.set(num + 1)
            
    def show(self):
        print(self.code)
        if self.next is not None:
            self.next.show()

Ag = Chain_mg("my_chain", 3)  # Создаем цепочку из трех объектов
Ag.set()  # Устанавливаем коды
Ag.show()  # Выводим коды
