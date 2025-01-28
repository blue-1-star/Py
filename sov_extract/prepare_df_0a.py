import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from openpyxl import load_workbook
import tempfile
import os
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.regression.mixed_linear_model import MixedLM
import pandas as pd

file = r"G:\My\sov\extract\FL for permuations.xlsx"
# file = r"G:\My\sov\extract\FL for mixed effect regression.xlsx"
output_dir = os.path.join(os.path.dirname(__file__), 'Data')

sheet_name = 0          #"Sheet1"
xls = pd.ExcelFile(file)
# Проверка на существование листа
if isinstance(sheet_name, int):
    if sheet_name >= len(xls.sheet_names):
        raise ValueError("Лист с указанным индексом не существует.")
    sheet_name = xls.sheet_names[sheet_name]
else:
    if sheet_name not in xls.sheet_names:
        raise ValueError(f"Лист с именем '{sheet_name}' не найден. Доступные листы: {xls.sheet_names}")

df = xls.parse(sheet_name="Sheet1")
df = df.drop(columns='Combined Yield')

df = (
    df.rename(columns={df.columns.values[0]: 'Method'})  # Переименование столбца
      .assign(Method=lambda x: 'method_' + x['Method'].astype(str))  # Добавляем префикс method_
)
# df = add_phase_column(df)
# Преобразование столбцов в категориальный тип
df = df.assign(
    Method=df['Method'].astype('category'),
    Solvent_Type=df['Solvent'].astype('category'),
    Extraction_Technique=df['Extraction Technique'].astype('category')
)

# Реализация эквивалента
df1 = (
    df.drop(columns=['Replicate Number'])  # Удаляем старый столбец
        .groupby('Method', group_keys=False)  # Группировка по 'Method'
        .apply(lambda group: group.assign(Replicate=pd.Categorical(group.reset_index().index + 1)))  # Создаем новый столбец 'Replicate'
)

print(df1)
# Определяем столбцы, которые нужно оставить без изменений
id_vars = ['Method', 'Solvent_Type', 'Extraction_Technique', 'Replicate']
# Определяем только те столбцы, которые нужно трансформировать
value_vars = [col for col in df1.columns if col.startswith('Measurement')]

dataTall = pd.melt(
    df1,
    id_vars=id_vars,  # Оставляем эти столбцы как есть
    value_vars=value_vars,  # Преобразуем только Measurement 1, 2, 3
    var_name='Measurement',  # Название столбца для имен измерений
    value_name='carbs/mg'    # Название столбца для значений
)


output_file = os.path.join(output_dir, f"test_.xlsx")
dataTall.to_excel(output_file)


def f_out(outfile):
    """
    Формирует путь для файла в подкаталоге 'Data' текущего каталога,
    добавляя текущую дату к имени файла перед расширением.
    
    Parameters:
        outfile (str): Имя исходного файла (например, "output.pdf").
    
    Returns:
        str: Полный путь к файлу в формате "Data/<имя>_<дата>.<расширение>".
    """
    # Получаем текущую дату
    current_date = datetime.now().strftime("%d_%m")
    
    # Создаем директорию Data, если ее нет
    # Определяем рабочую директорию (используем os.getcwd() вместо __file__)
    # output_dir = os.path.join(os.getcwd(), 'Data')
    output_dir = os.path.join(os.path.dirname(__file__), 'Data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Разделяем имя файла и расширение
    base_name, ext = os.path.splitext(outfile)
    
    # Формируем новое имя файла с добавлением даты
    output_file = os.path.join(output_dir, f"{base_name}_{current_date}{ext}")
    
    return output_file

def lin_r(dataTall):
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    # Регрессионная модель
    formula = 'Q("carbs/mg") ~ C(Method) + C(Solvent_Type) + C(Extraction_Technique)'
    model = ols(formula, data=dataTall).fit()
    # print(model.summary())
    return(model.summary())
res_lin_r = lin_r(dataTall)

# print( res_lin_r)
with open(f_out("res_lin_r.txt"), "w") as file:
    # Перенаправляем вывод в файл
    print(res_lin_r, file=file)
# plot_gr(dataTall,output_dir)
# formula = 'Q("carbs/mg") ~ C(Solvent_Type) + C(Extraction_Technique)'

# Подготовка данных (аналог rename и mutate)
dataReg = dataTall.rename(
    columns={'Solvent_Type': 'Solvent', 
             'Extraction_Technique': 'Extraction', 
             'carbs/mg': 'Concentration'}
)
dataReg['Measurement'] = dataReg['Measurement'].astype('category')

# Создание смешанной модели
# formula = 'Concentration ~ C(Solvent) + C(Extraction) + C(Method)'
# mixed_model = MixedLM.from_formula(
#     formula,
#     groups=dataReg['Replicate'],  # Случайный эффект для Replicate
#     data=dataReg
# )
# Отладочный вывод
print(dataReg.describe())
print(dataReg.info())
print("Количество уникальных значений в группах (Replicate):", dataReg['Replicate'].nunique())
print(dataReg.groupby('Replicate').size())  # Проверить равномерность распределения групп
print(dataReg.isna().sum())  # Проверить пропущенные значения
# коллинеарность
from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrices

# Создаем матрицу дизайна для предикторов
_, X = dmatrices('Concentration ~ C(Solvent) + C(Extraction) + C(Method)', data=dataReg, return_type='dataframe')

# Вычисляем VIF для каждого предиктора
vif = pd.DataFrame({
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
    'Predictor': X.columns
})
print(vif)
# 

formula = 'Concentration ~ C(Solvent) + C(Extraction)'
mixed_model = MixedLM.from_formula(
    formula,
    groups=dataReg['Replicate'],  # Случайный эффект для Replicate
    data=dataReg
)
# 3. Проверить распределение случайных эффектов
print(dataReg.groupby('Replicate')['Concentration'].mean())  # Средние по группам
print(dataReg.groupby('Replicate')['Concentration'].std())   # Стандартные отклонения по группам


# Подгонка модели
result = mixed_model.fit()

print(result.summary())
with open(f_out("mix_lin_r.txt"), "a") as file:
    # Перенаправляем вывод в файл
    print(result.summary(), file=file)
    print(result.params, file=file)  # Все коэффициенты
    print(result.model.exog_names, file=file)  # Названия переменных (включая baseline)

