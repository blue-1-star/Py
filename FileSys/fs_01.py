from pathlib import Path
p = Path('.')
ld= [x for x in p.iterdir() if x.is_dir()]
print(ld)


