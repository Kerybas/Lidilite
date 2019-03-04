import lidilite
import sqlite3
import json

# Loading data from a json. It's designed having REST API in mind.
with open('example_data.json') as f:
    data = json.load(f)
print('Data used as example:')
for row in data:
    print(row)

# Suggest a CREATE TABLE query statement
create_query = lidilite.draft_create_table(data, table_name='TABLE_1', mode='all', primary_keys='id')
print('\nSuggested CREATE query:\n', create_query)

# Use the suggested query to create a table in a SQLite3 database, in memory
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute(create_query)

# Insert data in the table
table = lidilite.Table(conn, 'TABLE_1')
table.insert(data)

# Confirm data is there
print('\nData loaded in table:\n', cur.execute('SELECT * FROM TABLE_1').fetchall())

# Replace data in the table
new_data = [{"id": "A00001", "color": "dark blue", "count": 3, "size": 1.6, "content": "no more stuff"}]
table.replace(new_data)

# Confirm data is replaced
print('\nData after update:\n', cur.execute('SELECT * FROM TABLE_1').fetchall())
