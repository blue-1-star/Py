import tkinter as tk

def create_gui():
    # Создание главного окна
    root = tk.Tk()
    root.title("Пример использования enumerate и grid")

    # Список заголовков
    headers = ["Header1", "Header2", "Header3"]

    # Создание и размещение меток
    for col_num, header in enumerate(headers, 0):
        # tk.Label(root, text=header).grid(row=2, column=col_num, padx=5, pady=5)
        tk.Label(root, text=header).grid(row=0, column=col_num, padx=5, pady=5)

    # Запуск главного цикла приложения
    root.mainloop()

# Вызов функции для создания GUI
create_gui()
