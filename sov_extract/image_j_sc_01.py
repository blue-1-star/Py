from ij import IJ
from ij.io import DirectoryChooser
from ij.plugin.frame import RoiManager
import os

# 1. Выбор папки с изображениями
dc = DirectoryChooser("Выберите папку с изображениями")
folder = dc.getDirectory()
if folder is None:
    IJ.log("Папка не выбрана!")
    exit()

# 2. Если у вас известны параметры масштаба, задайте их в этой строке.
#    Например: 100 пикселей соответствуют 5 см, единица измерения — см.
#    Команда Set Scale в ImageJ требует: distance=100 known=5 pixel=1 unit=cm
scaleString = "distance=100 known=5 pixel=1 unit=cm"

# 3. Получаем список файлов с нужными расширениями (JPG, PNG, TIFF и т.п.)
files = os.listdir(folder)
imageFiles = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff"))]
if not imageFiles:
    IJ.log("Не найдено файлов изображений в папке!")
    exit()

# 4. Создаём экземпляр ROI Manager (если его ещё нет)
rm = RoiManager.getInstance()
if rm is None:
    rm = RoiManager()

# 5. Перебор всех файлов изображений в папке
for f in imageFiles:
    # Полный путь к файлу
    path = os.path.join(folder, f)
    
    # Открываем изображение
    imp = IJ.openImage(path)
    if imp is None:
        IJ.log("Не удалось открыть файл: " + f)
        continue
    imp.show()  # показываем изображение

    # 5.1. Устанавливаем масштаб автоматически (если scaleString корректен)
    IJ.run(imp, "Set Scale...", scaleString)
    
    # 5.2. Информируем пользователя: вручную выделите нужную область и нажмите OK
    IJ.waitForUser("Выделите область", 
                   "Пожалуйста, выделите область ячейки чашки Петри, затем нажмите OK.")
    
    # 5.3. Получаем выделенную область (ROI)
    roi = imp.getRoi()
    if roi is None:
        IJ.log("ROI не выбрана для изображения: " + f)
    else:
        # Добавляем ROI в ROI Manager для дальнейшего анализа или сохранения
        rm.addRoi(roi)
        
        # Пример: измеряем параметры выделенной области
        IJ.run(imp, "Measure", "")
        IJ.log("Измерения для " + f + " выполнены.")
    
    # 5.4. Закрываем изображение, чтобы открыть следующее
    imp.changes = False  # если не требуется сохранять изменения
    imp.close()

# После обработки всех изображений можно показать окно ROI Manager с полученными ROI.
rm.runCommand("Show All")
IJ.log("Обработка завершена!")
