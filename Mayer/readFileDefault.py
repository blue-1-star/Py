import os
cd = os.getcwd()
filename = "readFileDefault.py" # этот код
file_path = os.path.join(cd, filename)
f = open(file_path)
lines = []
for line in f:
 lines.append(line.strip())
print(lines)
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
