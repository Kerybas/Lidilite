# Lidilite  

Lidilite (**Li**st **Di**ct to SQ**Lite**) simplifies the operation of 
writing lists of dictionaries into a sqlite database.  

Once connected to a sqlite3 table, Lidilite inserts or replaces all the
elements of a list of dictionaries that can fit in the sqlite3 table.  
If dict keys do not exist in the table, they are ignored.  
If keys are missing from a dictionary, NULL values are passed.  

##### Example of Lidilite.Table:

```python
import lidilite
import sqlite3

data = [
    {'id':'A00001','color':'blue', 'count':3, 'size': 1.6, 'content':['stuff1','stuff2']},
    {'id':'A00002','color':'red', 'count':6, 'size': 2, 'content':[]},
    {'id':'A00003', 'count':3, 'size': 1.6},
    {'id':'A00004','color':'green', 'count':0, 'size': 7.4, 'content':['stuff1','stuff2','stuff4']},   
]

cnx = sqlite3.connect('test.db')
table = lidilite.Table(cnx, 'TABLE_1')

table.insert(data)
```
```sql
SELECT * FROM TABLE_1

id      color	count	size	content
A00001	blue	3	1.6	['stuff1', 'stuff2']
A00002	red	6	2.0	[]
A00003		3	1.6	
A00004	green	0	7.4	['stuff1', 'stuff2', 'stuff4']
```
Lidilite also provides a tool to print out a CREATE query that would match
the given list of dictionaries.  

##### Example of Lidilite.draft_create_query:
```python
import lidilite
data = [
    {'id':'A00001','color':'blue', 'count':3, 'size': 1.6, 'content':['stuff1','stuff2']},
    {'id':'A00002','color':'red', 'count':6, 'size': 2, 'content':[]},
    {'id':'A00003', 'count':3, 'size': 1.6},
    {'id':'A00004','color':'green', 'count':0, 'size': 7.4, 'content':['stuff1','stuff2','stuff4']},   
]

create_query = lidilite.draft_create_query(data, table_name='TABLE_1', mode='all')
print(create_query)
```
```sql
CREATE TABLE "TABLE_1" (
	"id"	TEXT,
	"color"	TEXT,
	"count"	INTEGER,
	"size"	REAL,
	"content"	TEXT);
```

