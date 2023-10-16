# ex 04 ch 03  p 170
# Напишите программу, в которой есть функция для заполнения вложенного списка.
# Список заполняется натуральными числами «змейкой»: сначала заполняется первая строка,
# затем последний столбец(сверху вниз), последняя строка (справа налево), первый столбец
# (снизу вверх), вторая строка (слева направо), и так далее.
def fill(m,n):
    A = [[m*(j) + (i+1) for i in range(m)]  for j in range(n)]
    return A
def show(A):
    for a in A:
        for s in a:
            print(s, end=" ")
        print()  
def fill_snake_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    num = 1
    top, bottom, left, right = 0, n - 1, 0, n - 1

    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            matrix[top][i] = num
            num += 1
        top += 1

        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num += 1
        right -= 1

        for i in range(right, left - 1, -1):
            matrix[bottom][i] = num
            num += 1
        bottom -= 1

        for i in range(bottom, top - 1, -1):
            matrix[i][left] = num
            num += 1
        left += 1

    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

n = int(input("Введите размер матрицы: "))
snake_matrix = fill_snake_matrix(n)
print_matrix(snake_matrix)


# A = fill(4,3)
# show(A)

