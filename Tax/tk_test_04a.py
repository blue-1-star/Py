import tkinter as tk

def create_gui():
    # Создание главного окна
    root = tk.Tk()
    root.title("Пример использования row в grid")

    # Список заголовков
    headers = ["Header1", "Header2", "Header3"]

    # Создание и размещение меток в другой строке
    for col_num, header in enumerate(headers, 0):
        tk.Label(root, text=header, borderwidth=2, relief="solid").grid(row=1, column=col_num, padx=5, pady=5)

    # Добавление дополнительных виджетов для сравнения
    tk.Label(root, text="Content 1", borderwidth=2, relief="solid").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(root, text="Content 2", borderwidth=2, relief="solid").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(root, text="Content 3", borderwidth=2, relief="solid").grid(row=0, column=2, padx=5, pady=5)

    # Добавление кнопки для наглядности
    tk.Button(root, text="Button", borderwidth=2, relief="solid").grid(row=2, column=1, padx=5, pady=5)

    # Запуск главного цикла приложения
    root.mainloop()

# Вызов функции для создания GUI
create_gui()
