# Lidilite  

Lidilite (**Li**st **Di**ct to SQ**Lite**) simplifies the operation of 
writing lists of dictionaries into a SQLite database.  
It is particularly handy when you work with json data coming from APIs. You can easily populate your table with `Table.insert` or `Table.replace`.  
If you are just starting your project and do not have a SQLite table yet, you can use your data to draft the SQL `CREATE` query with `draft_create_table`.

## Examples
You have a list of dictionaries `data` that you want to store in `TABLE_1` of `database.db`:  
```python
cnx = sqlite3.connect('database.db')
table = lidilite.Table(cnx, 'TABLE_1')
table.insert(data)
```

You have a `new_data`, including some elements that should replace previously loaded data:
```python
table.replace(new_data)
```
*Note: this requires a primary key in your table otherwise it acts like `insert`*  

You don't have a SQLite table yet?  
You can draft a SQLite query to create the table matching your `data`:
```python
query = lidilite.draft_create_table(data, table_name='TABLE_1', primary_keys='id')
print(query)
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
See example.py for a complete demo.  

## Documentation
#### `lidilite.Table(connexion, table)`  
The main object representing the table to be modified.  
+ `connexion`: a sqlite3.connect(database) object  
+ `table`: the name of the target table  

---
#### `lidilite.Table.insert(data_list_dicts)`
+ `data_list_dicts`: a list of dictionaries to be inserted in the table.  

All dicts do not have to have the same structure. If a key is missing in a dict, a `None` value will
be passed to the table.  
If a key exist in a dictionary but not in the table, it will be ignored.  
Value types are controled and forced to int, float or string. Boolean are converted in in 1 or 0, as 
it is done by sqlite3 anyway.  
Empty list or dict are passed as strings `"[]"` or `"{}"`.  

---
#### `lidilite.Table.replace(data_list_dicts)`
+ `data_list_dicts`: a list of dictionaries to be replaced or inserted in the table.  

If the table does not have a primary key or matching keys are not found in the table, it acts as `insert`.  
Otherwise, it overwrites the rows with matching keys.  

---
#### `lidilite.draft_create_table(data_list_dicts, table_name='NEW_TABLE', mode='all', primary_keys=None)`  
+ `data_list_dicts`: a list of dictionaries representing the dataset to be loaded in the table.  
+ `table_name`: the name of your table.  
+ `mode`: either `all` or `common`.  
	- `all` is to create a table including all possible columns found in the dataset.
If a key appears at least one time in the list of dicts, it will generate a column.  
	- `common` is to create a table including only columns that are found in every dictionary.  
+ `primary_keys`: A single primary key as a string or a list of primary keys, or nothing.  

It returns a string that you can potential pass to a sqlite3 cursor(), see `examples.py`.  
However, I prefer reviewing the query and passing it manually in [DB Browser for SQLite](https://sqlitebrowser.org/).
