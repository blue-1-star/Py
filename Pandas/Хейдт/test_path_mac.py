from pathlib import Path
import pandas as pd
# Получаем путь к папке, где лежит текущий скрипт
SCRIPT_DIR = Path(__file__).parent
# print( SCRIPT_DIR)
# Строим путь к данным
DATA_PATH = SCRIPT_DIR / "Data" / "sp500.csv"
df = pd.read_csv(DATA_PATH)
print(df)