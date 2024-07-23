import tkinter as tk
from tkinter import StringVar

def create_gui():
    # Создание главного окна
    root = tk.Tk()
    root.title("Пример использования grid_forget")

    # Создание объектов StringVar
    income_var = StringVar()
    expense_var = StringVar()

    # Создание виджетов и связывание с StringVar
    tk.Label(root, text="Доход:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=income_var, width=30).grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Расход:").grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(root, textvariable=expense_var, width=30).grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Дополнительные данные:").grid(row=2, column=0, padx=10, pady=10)
    tk.Entry(root, width=30).grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="Удаляемая строка 1").grid(row=3, column=0, padx=10, pady=10)
    tk.Entry(root, width=30).grid(row=3, column=1, padx=10, pady=10)

    tk.Label(root, text="Удаляемая строка 2").grid(row=4, column=0, padx=10, pady=10)
    tk.Entry(root, width=30).grid(row=4, column=1, padx=10, pady=10)

    # Функция для удаления строк
    def delete_rows():
        for widget in root.grid_slaves():
            if int(widget.grid_info()["row"]) > 2:
                widget.grid_forget()

    # Кнопка для вызова функции delete_rows
    tk.Button(root, text="Удалить строки", command=delete_rows).grid(row=5, column=0, columnspan=2, pady=10)

    # Запуск главного цикла приложения
    root.mainloop()

# Вызов функции для создания GUI
create_gui()
