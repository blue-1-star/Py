# p 209  для  текстового значения определяются гласные буквы, представленные во введенном тексте.
Sr = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
Se = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
vowels_r = {"А", "Е", "Ё", "И", "О", "У", "Ы", "Э", "Ю", "Я"}
vowels_e = {"A", "E", "I", "O", "U", "Y", "W"}
text = "осень настала холодно стало ё"
text_e = "Autumn has come and it's cold." 
A = set(text.upper())
Ae = set(text_e.upper())
res = vowels_r & A
res_e = vowels_e & Ae
print("Result:", res)
print("Result: eng", res_e)




