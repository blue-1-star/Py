# В строке по сравнению с исходной символы меняются местами «через один»: первый символ
# меняется местами с третьим, четвертый символ меняется местами с шестым, седьмой меняется местами с девятым
txt = "В строке по сравнению с исходной символы меняются местами"
txt1 ="собаки_ -"
def swap_ch(txt, i,j):
    if 0 <= i < len(txt) and 0 <= j < len(txt):
        # Создаем новую строку, объединяя части исходной строки
        sw_str =txt[:i] + txt[j] +txt[i+1:j] + txt[i] + txt[j+1:]
        return sw_str
    else:
        return txt
cur_txt, c_txt = "",""       
# A=[i for i in range(len(txt)) if i%3==0]
# for i in A:
#     cur_txt = swap_ch(txt,i,i+2) 
#     c_txt += cur_txt[i:i+3]

c_txt = ''.join([swap_ch(txt, i, i+2)[i:i+3] for i in range(len(txt)) if i % 3 == 0])
print(txt)    
print(c_txt)


