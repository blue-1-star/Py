# каждая буква заменяется на ту, что размещена от нее на две позиции влево.
#  Вторая буква в алфавите заменяется на последнюю. Первая буква в алфавите заменяется на предпоследнюю.
txt = " самый надежный шифр на белом свете с черной магией"
first_ch_code = 1040
second_ch_code = 1041
last_ch_code = 1071   # code last russian  char  
penultimate_ch_code = 1070
def encr_m2(txt):
    tx="" 
    for c in txt:
        ch=chr(ord(c)-2)
        if ord(c) == second_ch_code:
            ch=chr(last_ch_code)
        elif ord(c) == first_ch_code:
            ch=chr(penultimate_ch_code)
        tx+=ch
    return tx
def dcr_m2(txt):
    tx="" 
    for c in txt:
        ch=chr(ord(c)+2)
        if ord(c) == last_ch_code:
            ch=chr(second_ch_code)
        elif ord(c) == penultimate_ch_code:
            ch=chr(first_ch_code)
        tx+=ch
    return tx
etxt = encr_m2(txt)
print(etxt.lower())
detxt = dcr_m2(etxt)
print(detxt.lower())
