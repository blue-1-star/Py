# p 65  chapter 3
tup = 4,5,6
print(tup)
# Распаковка кортежей
tup = (4, 5, 6)
a, b, c = tup
print(f'{a},{b},{c}')
seq = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
for a, b, c in seq:
    print(f'a={a}, b={b}, c={c}')
values = 1, 2, 3, 4, 5
a, b, *rest = values   
print(f'a={a}, b={b}, rest = {rest}')
seq = [7, 2, 3, 7, 5, 6, 0, 1]
seq[3:5] = [6, 3]
print(seq)
print(seq[::-1])
seq[-4:]


