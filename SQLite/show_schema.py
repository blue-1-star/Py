import sqlite3

db = r"G:\Programming\Py\OSBB\Data\db\osbb_test.db"

con = sqlite3.connect(db)

cur = con.execute("""
SELECT sql
FROM sqlite_master
WHERE type='table'
AND name='payments'
""")

# file = cur.fetchone()[0]
print(cur.fetchone()[0])

con.close()