"""
Gpt about StringVar, IntVar ...
В этом примере:
Мы создаем главное окно root и строковую переменную color.
Устанавливаем начальное значение переменной в "red".
Создаем виджет Entry (текстовое поле), связываем его с
переменной color с помощью textvariable. Создаем функцию on_variable_change,
которая будет вызываться при изменении значения переменной color.
В данном случае, она просто выводит новое значение переменной в консоль.
С помощью trace_add("write", on_variable_change) мы привязываем функцию 
on_variable_change к переменной color. Таким образом, каждый раз, когда значение переменной color изменяется, будет вызвана функция on_variable_change.
Теперь, если вы вводите новое значение в текстовое поле (Entry), функция on_variable_change будет вызываться, и новое значение 
будет выводиться в консоль.

"""
from tkinter import *

def on_variable_change(*args):
    new_value = color.get()
    print("Variable changed! New value:", new_value)

root = Tk()

color = StringVar()
color.set("red")  # Устанавливаем начальное значение переменной

entry = Entry(root, textvariable=color)
entry.pack(pady=10)

color.trace_add("write", on_variable_change)

root.mainloop()
