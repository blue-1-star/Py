import pandas as pd
import numpy as np
import re

# Задаем пути к файлам
data_xy_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\result.xlsx"
data_scale_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\spores_main.xlsx"

# Чтение Excel-файлов
data_XY = pd.read_excel(data_xy_path)
data_Scale = pd.read_excel(data_scale_path)
print(data_Scale.columns)
print(data_XY.columns)
# Извлечение базового имени из столбца Image (удаляем расширение)
data_XY['BaseName'] = data_XY['Image'].str.replace(r'\.[^.]+$', '', regex=True)

# Выполнение объединения: левое соединение (left join)
# Таким образом, все записи из data_XY сохранятся, а соответствующий Scale подтянется из data_Scale
merged_data = pd.merge(data_XY, data_Scale, left_on='BaseName', right_on='File', how='left')
merged_data.rename(columns={'pix/mm': 'Scale'}, inplace=True)

# Вычисление геометрических характеристик для каждой споры
merged_data['Length_X'] = abs(merged_data['X2'] - merged_data['X1'])
merged_data['Length_Y'] = abs(merged_data['Y2'] - merged_data['Y1'])
merged_data['Diameter'] = np.sqrt(merged_data['Length_X'] * merged_data['Length_Y'])
merged_data['Area'] = np.pi * merged_data['Length_X'] * merged_data['Length_Y'] / 4

# Сохранение измененного файла data_XY с суффиксом _calc
output_xy_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\data_XY_calc.xlsx"
merged_data.to_excel(output_xy_path, index=False)
