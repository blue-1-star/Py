

def merge_rows_by_fraction(df):
    # Функция для суммирования с учетом прекращения при невозрастании i
    # Создаем копию датафрейма, чтобы избежать изменений в оригинале
    df = df.copy()
    
    # Разделяем столбец Num_in на целую и дробную часть
    df[['n', 'i']] = df['Num_in'].astype(str).str.split('.', expand=True)
    
    # Преобразуем столбец n в целочисленный тип
    df['n'] = df['n'].astype(int)
    
    # Если дробная часть отсутствует, присваиваем ей значение 1
    df['i'] = df['i'].replace({None: '1', '0': '1'}).astype(int)
   
     
    # Сохраняем индекс как столбец
    df['original_index'] = df.index

    def cumulative_sum_with_stop(group):
        sum_part = 0
        w_sum = []
        for idx in range(len(group)):
            if idx == 0 or group['i'].iloc[idx] > group['i'].iloc[idx - 1]:
                sum_part += group['w_part'].iloc[idx]
            else:
                sum_part = group['w_part'].iloc[idx]
            w_sum.append(sum_part)
        return w_sum
    
    # Применяем группировку и кумулятивное суммирование
    df['w_sum'] = df.groupby(['n', 'Treat_N'], group_keys=False).apply(
        lambda x: x.assign(w_sum=cumulative_sum_with_stop(x)))['w_sum']

    # Оставляем только строки с минимальной дробной частью для каждой группы
    df = df.loc[df.groupby(['n', 'Treat_N'])['i'].idxmin()]
    # Восстанавливаем порядок строк по оригинальному индексу
    df = df.sort_values(by='original_index').drop(columns=['original_index'])
    
    # Удаляем вспомогательные столбцы
    df.drop(columns=['n', 'i'], inplace=True)
    
    return df


pd.set_option('display.max_rows', None)  # Показать все строки
pd.set_option('display.max_columns', 5)  # Показать все столбцы (4)


file_path = r"G:\My\sov\extract\weights.xlsx"
sheet_name = "Sheet1"
columns_rename = ['Treat_N', 'Num_in', 'Ex_ph_1','Ex_ph_2','w_part','w_sum','w_av', 'std']
df = read_sheet01(file_path)
ind_fill = [1,2,3]
df = fill_nan_with_previous(df, ind_fill)

df1 = count_transitions_with_tracking(df, 1, 0)

print(f"data = {df1}")
df1.columns = columns_rename
strf, strr  = 'ethanol 80%', 'et_80'
replace_list = [('ethanol 80%', 'et_80'), ('HCl 0.1 M', 'HCl')]
df1 = replace_text_in_columns(df1, [2,3], replace_list)
print(f"data = {df1.iloc[:, [0,2,3,5]]}")
df2 = merge_rows_by_fraction(df1)
print(f"df2 = {df2.iloc[:, [0,2,3,5]]}")

#
#
"""
алгоритм слияния строк ( результаты опыта собраны в нескольких пробирках от 1 до 3 - номера пробирок 
отображены вторым числом (можно считать дробная часть) после точки в столбце 1  (Num_in)  n.i1, n.i2,... )
1. для дробных частей одного и того же целого n столбца 1 (w_part) суммируются значения    n.i1, n.i2, ... 
    сумма заносится в столбец 5 ( w_sum)
    строки со значениями n.i2, ... в столбце 1 (Num_in) удаляются. Из группы n остается только одна строка n.i1  
Проход по всем строкам столбца 1  (w_part)


"""