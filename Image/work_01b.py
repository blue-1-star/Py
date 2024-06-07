import matplotlib.pyplot as plt
from PIL import Image

# Загрузка изображения
im_path ="G:/Programming/Py/Image/data/"
# filename = "id_cod_e.bmp"
filename = "id_cod.bmp"
image_path = im_path + filename 
image = Image.open(image_path)

# Функция для обработки кликов мыши
coords = []

def onclick(event):
    global coords
    ix, iy = event.xdata, event.ydata
    coords.append((ix, iy))
    if len(coords) == 2:
        plt.close()

# Отображение изображения и установка обработчика событий
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
ax.imshow(image, cmap='gray')
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

print(coords)
