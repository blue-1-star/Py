import cv2
import numpy as np
import matplotlib.pyplot as plt
# Загрузка изображения
file_image = r"G:\My\sov\extract\Spores\original_img\test\best\4x\A best_4x_1_scale.png"
img = cv2.imread(file_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

plt.figure(figsize=(8, 6))
plt.imshow(blur, cmap="gray")
plt.title("Gaussian Blurred Image")
plt.axis("off")
plt.show()
