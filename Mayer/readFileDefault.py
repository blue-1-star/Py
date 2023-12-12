import os

# Получаем путь к директории, содержащей этот скрипт
script_directory = os.path.dirname(os.path.abspath(__file__))
print("Script directory:", script_directory)

filename = "readFileDefault.py"
file_path = os.path.join(script_directory, filename)
lines = []
with open(file_path, 'r') as f:
    for line in f:
        lines.append(line.strip())
        print(lines)
    # Ваш код работы с файлом
    pass


# print("Current directory:",cd)
# filename = "readFileDefault.py" # этот код
# file_path = os.path.join(cd, filename)
# f = open(file_path)
"""
['filename = "readFileDefault.py" # этот код',
'',
'f = open(filename)',
'lines = []',
'for line in f:',
'lines.append(line.strip())',
'',
'print(lines)']
"""
# G:\Programming\Py\Mayer\readFileDefault.py