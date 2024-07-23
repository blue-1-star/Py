import tkinter as tk
from tkinter import StringVar

def create_gui():
    # Создание главного окна
    root = tk.Tk()
    root.title("Пример использования columnspan")

    # Создание объектов StringVar
    income_var = StringVar()
    expense_var = StringVar()

    # Создание виджетов и связывание с StringVar
    tk.Label(root, text="Доход:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=income_var, width=30).grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Расход:").grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=expense_var, width=30).grid(row=1, column=1, padx=10, pady=10)

    # Создание кнопки, которая будет занимать два столбца
    tk.Button(root, text="Показать значения", command=lambda: print("Доход:", income_var.get(), "Расход:", expense_var.get())).grid(row=2, column=0, columnspan=2, pady=10)

    # Запуск главного цикла приложения
    root.mainloop()

# Вызов функции для создания GUI
create_gui()
