# Lidilite  

Lidilite (**Li**st **Di**ct to SQ**Lite**) simplifies the operation of 
writing lists of dictionaries into a sqlite database.  

You have a list of dictionaries, that you want to store in a sqlite database?
```python
cnx = sqlite3.connect('database.db')
table = lidilite.Table(cnx, 'TABLE_NAME')
table.insert(data)
```
Your table has a primary key and you want to replace some rows?
```python
table.replace(data)
```

You don't have a sqlite table yet?  
You have a list of dictionaries and want to initialize the sqlite table?
```python
query = lidilite.draft_create_table(data, table_name='TABLE_NAME', primary_keys='id')
```
```sql
 CREATE TABLE "TABLE_1" (
	"id"	TEXT,
	"color"	TEXT,
	"count"	INTEGER,
	"size"	REAL,
	"content"	TEXT,
	PRIMARY KEY("id"));
```