"""
 создается новый текст, в котором по сравнению с исходным
удалено самое длинное и самое короткое слово. Если таких слов несколько, 
то удаляется первое из них. Под словами подразумевать блоки
текста, разделенные пробелами.
"""
txt = "создается новый текст, в котором по сравнению с исходным \
удалено самое длинное и самое короткое слово. Если таких слов несколько, то удаляется первое из них. \
 Под словами подразумевать блоки \
текста, разделенные пробелами."
txl = txt.split()
print(txl)
# create dictionary key - word : value - len(word) from list txl
D = {word:len(word) for word in txl }
print(D)
print("Number=", len(D))
min_value = min(D.values())
max_value = max(D.values())
print(min(D.values()), max(D.values()))
key_to_del_min = [key for key, value in D.items() if value == min_value][0]
key_to_del_max = [key for key, value in D.items() if value == max_value][0]

del D[key_to_del_min]
# del D[key_to_del_min, key_to_del_max]
del D[key_to_del_max]
print("Number=", len(D))
print(D)
txl_key = [k for k in D]
print(txl_key,"\n",len(txl_key))
# method keys:
txl_key1 = D.keys()
print("Method keys\n",txl_key1,"\n",len(txl_key))
def min_key(D):    #  returns the key of the minimum dictionary value
    min_value = min(D.values())
    key_min = [key for key, value in D.items() if value == min_value][0]
    return key_min
def max_key(D):    #  returns the key of the maximum dictionary value
    max_value = max(D.values())
    key_max = [key for key, value in D.items() if value == max_value][0]
    return key_max
