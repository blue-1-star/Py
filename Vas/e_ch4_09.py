"""
Напишите программу, в которой пользователю предлагается ввести текстовое значение. На основе текста формируется словарь. Ключами элементов словаря являются символы из текста. Значение соответствующего элемента — это исходный текст, в котором «вычеркнут»
тот символ, который является ключом. Если при формировании очередного элемента словаря окажется, что такой ключ уже есть, то соответствующий символ пропускается. Например, если пользователь ввел
текст "ABCABD", то в словаре будут представлены элементы с ключами
"A", "B", "C" и "D" со значениями соответственно "BCABD", "ACABD",
"ABABD" и "ABCAB".
"""
txt = "ИНСУМИНИН"
S = set(txt)
D=dict()
for s in S:
    Tl=list(txt)
    Tl.remove(s)
    D[s]=''.join(Tl) # операция слияния списка в текст '' - без разделителя 
print(D)
