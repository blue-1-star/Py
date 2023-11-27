"""
с помощью главного меню выбирать название животного, и картинка с этим животным отобража-
ется в окне.
"""
# Version GPT 
from tkinter import *

def show_image(animal):
    selected_index = animals.index(animal)
    img_label.configure(image=imgs[selected_index])

root = Tk()
root.title("Animal Viewer")

W, H = 800, 600
Swh = f"{W}x{H}"
root.geometry(Swh)

# Меню
menu_bar = Menu(root)
root.config(menu=menu_bar)

animal_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Select Animal", menu=animal_menu)

animals = ["Cat", "Tiger", "Pig Snout"]
for animal in animals:
    animal_menu.add_command(label=animal, command=lambda a=animal: show_image(a))

# Картинки
path="G:\\Programming\\Py\\Vas\\picture\\"   # Укажите путь к вашим изображениям
# files = ["cat.png", "tiger.png", "pig_snout.png"]
files=["cats_embrace_01.png","tiger1.png","Born_Wild_01.png"]  
imgs = [PhotoImage(file=path + f) for f in files]
# Отображение картинки
frm_img = Frame(root)
img_label = Label(frm_img)
img_label.pack()
frm_img.pack()
root.mainloop()
"""

В этом операторе используется цикл for для перебора каждого элемента animal в списке animals.
Для каждого элемента создается команда в подменю (animal_menu).

for animal in animals:
    animal_menu.add_command(label=animal, command=lambda a=animal: show_image(a))
Разберем каждую часть:
for animal in animals:: Это цикл, который итерирует по каждому элементу в списке animals.
Переменная animal принимает значение текущего элемента на каждой итерации.
animal_menu.add_command(...): Для каждого животного создается команда в подменю animal_menu.
label=animal: Это параметр, который устанавливает текст (название) команды в подменю на текущее значение animal.
command=lambda a=animal: show_image(a): Это параметр, который устанавливает функцию,
которая будет вызываться при выборе данной команды. Здесь используется анонимная функция (lambda),
которая принимает аргумент a и передает его функции show_image.
Важно заметить, что мы используем a=animal в lambda-функции для захвата значения animal на момент создания функции,
чтобы избежать проблемы с изменяемыми замыканиями.
Таким образом, каждое животное из списка становится командой в подменю,
и при ее выборе вызывается функция show_image, которая отображает соответствующую картинку.

"""