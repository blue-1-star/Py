import tkinter as tk

def create_gui():
    root = tk.Tk()
    root.title("Пример выделения строки")

    headers = ["Header1", "Header2", "Header3"]
    data = [
        ["Row1-Col1", "Row1-Col2", "Row1-Col3"],
        ["Row2-Col1", "Row2-Col2", "Row2-Col3"],
        ["Row3-Col1", "Row3-Col2", "Row3-Col3"]
    ]

    # Создание заголовков
    for col_num, header in enumerate(headers, 0):
        tk.Label(root, text=header, borderwidth=2, relief="solid").grid(row=0, column=col_num, padx=5, pady=5)

    # Создание строк данных
    for row_num, row_data in enumerate(data, 1):
        for col_num, cell_data in enumerate(row_data):
            tk.Label(root, text=cell_data, borderwidth=2, relief="solid").grid(row=row_num, column=col_num, padx=5, pady=5)

    # Функция для выделения строки
    def highlight_row(row):
        for col_num in range(len(headers)):
            cell = root.grid_slaves(row=row, column=col_num)[0]
            cell.config(bg="yellow")

    # Кнопка для выделения второй строки
    tk.Button(root, text="Выделить строку 2", command=lambda: highlight_row(2)).grid(row=4, column=0, columnspan=3, pady=10)

    root.mainloop()

create_gui()
