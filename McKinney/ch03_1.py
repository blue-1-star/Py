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
# p 74
tuples = zip(range(5), reversed(range(5)))
print(tuples)
mapping = dict(tuples)
print(mapping)
# p 75
words = ["apple", "bat", "bar", "atom", "book"]
by_letter = {}
by_letter1 = {}
for word in words:
    letter = word[0]
    if letter not in by_letter:
         by_letter[letter] = [word]
    else:
         by_letter[letter].append(word)
print(by_letter)    
from collections import defaultdict
by_letter1 = defaultdict(list)
for word in words:
    by_letter1[word[0]].append(word)
print(by_letter1)
# p 79
seq1 = ["foo", "bar", "baz"]
seq2 = ["one", "two", "three"]
zipped = zip(seq1, seq2)
print(list(zipped))
seq3 = [False, True]
print(list(zip(seq1, seq2, seq3)))
for index, (a, b) in enumerate(zip(seq1, seq2)):
    print(f"{index}: {a}, {b}")
# p 85
states = [" Alabama ", "Georgia!", "Georgia", "georgia", "FlOrIda",
"south carolina##", "West virginia?"]
import re
def clean_strings(strings):
    result = []
    for value in strings:
        value = value.strip()
        value = re.sub("[!#?]", "", value)
        value = value.title()
        result.append(value)
    return result
print(clean_strings(states))
def remove_punctuation(value):
    return re.sub("[!#?]", "", value)
clean_ops = [str.strip, remove_punctuation, str.title]
def clean_strings(strings, ops):
    result = []
    for value in strings:
        for func in ops:
            value = func(value)
        result.append(value)
    return result  
res = clean_strings(states, clean_ops)
print(res)      
# p 86
for x in map(remove_punctuation, states):
    print(x)
# p 87
def apply_to_list(some_list, f):
    return [f(x) for x in some_list]    
ints = [4, 0, 1, 5, 6]
res = apply_to_list(ints, lambda x: x * 2)
print(res)    
# отсортировать коллекцию строк по количеству различных букв в строке
strings = ["foo", "card", "bar", "aaaa", "abab"]
strings.sort(key=lambda x: len(set(x)))
print(strings)
# -----------
some_dict = {"a": 1, "b": 2, "c": 3}
for key in some_dict:
     print(key)
dict_iterator = iter(some_dict)
print(dict_iterator)     
print(list(dict_iterator))
# ---   p 88
def squares(n=10):
    print(f"Генерируются квадраты чисел от 1 до {n ** 2}")
    for i in range(1, n + 1):
        yield i ** 2
gen = squares()
for x in gen:
    print(x, end=" ")
gen = (x ** 2 for x in range(100))  # круглые скобки вместо квадратных
# ---- p 94
import sys
print(sys.getdefaultencoding())
# ----------
# 













