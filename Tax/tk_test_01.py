import tkinter as tk
from tkinter import StringVar

def create_gui():
    # Создание главного окна
    root = tk.Tk()
    root.title("Пример использования StringVar")

    # Создание объектов StringVar
    income_var = StringVar()
    expense_var = StringVar()

    # Настройки шрифта
    label_font = ('Helvetica', 14)
    entry_font = ('Helvetica', 14)

    # Создание виджетов и связывание с StringVar
    tk.Label(root, text="Доход:", font=label_font).grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=income_var, width=30, font=entry_font).grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Расход:", font=label_font).grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=expense_var, width=30, font=entry_font).grid(row=1, column=1, padx=10, pady=10)

    # Функция для отображения значений
    def show_values():
        print("Доход:", income_var.get())
        print("Расход:", expense_var.get())

    # Кнопка для вызова функции show_values
    tk.Button(root, text="Показать значения", command=show_values, font=label_font).grid(row=2, column=0, columnspan=2, pady=10)

    # Запуск главного цикла приложения
    root.mainloop()

# Вызов функции для создания GUI
create_gui()
