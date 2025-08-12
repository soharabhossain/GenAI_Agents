
# ERROR!!!!!!
# Unable to connect to the local DB file!!!!

import sqlite3

conn = sqlite3.connect("./storage/memory.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# View stored memory entries (assuming the table name is 'memory')
cursor.execute("SELECT * FROM memory;")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
