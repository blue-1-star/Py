#  каждая буква заменяется на следующую, а последняя буква в алфавите заменяется на первую. 
txt = " самый надежный шифр на белом свете с черной магией"
tx = txt.lower()
first_ch_code = 1040
last_ch_code = 1071   # code last russian  char  
# encrypt  
def encr_m1(txt):
    tx="" 
    for c in txt:
        ch=chr(ord(c)+1)
        if ord(c) == last_ch_code:
            ch=chr(first_ch_code)
        tx+=ch
    return tx
def dcr_m1(txt):
    tx="" 
    for c in txt:
        ch=chr(ord(c)-1)
        if ord(c) == first_ch_code:
            ch=chr(last_ch_code)
        tx+=ch
    return tx
etxt = encr_m1(tx)
print(etxt)
detxt = dcr_m1(etxt)
print(detxt)
