# Lidilite  

Lidilite (**Li**st **Di**ct to SQ**Lite**) simplifies the operation of 
writing lists of dictionaries into a SQLite database.  
It is particularly handy when you work with json data coming from APIs. You can easily populate your table with `Table.insert` or `Table.replace`.  
If you are just starting your project and do not have a SQLite table yet, you can use your data to draft the SQL `CREATE` query with `draft_create_table`.

**Installation:** `pip install lidilite`

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

#### `Table(connexion, table):`
Main object representing a sqlite3 table.  
`connexion:` a sqlite3.connect() object  
`table:` (str) the name of the target table

#### `Table.insert(data):`
Load a dataset of dicts in INSERT mode  
`data:` (list of dict) a dataset to be loaded in the table.

#### `Table.replace(data):`
Load a dataset of dicts in REPLACE mode  
`data:` (list of dict) a dataset to be loaded in the table.

#### `draft_create_table(data, table_name='NEW_TABLE', mode='all', primary_keys=None):`
This function takes a dataset (list of dicts) and returns a string representing
a SQLite `CREATE TABLE` query, matching the dataset structure.  
`data:` (list of dicts) the dataset you plan to insert in a SQLite table.  
`param table_name:` (str) the name of your SQLite table  
`param mode:` (str) either 'all' or 'common'.  
- **'all':** create a table including all possible columns found in the dataset.
                    If a key appears at least one time in the list of dicts, it will generate a column.
- **'common':** create a table including only columns that are found in every dictionary.
                   If a key appears only in a few dicts, it will not generate a column.
`param primary_keys:` (str, list, or None) either a single primary key, a list of primary keys, or nothing.

`return:` (str) a SQLite CREATE TABLE query, that you can potential pass to a sqlite3 cursor(), see `examples.py`.  
However, I prefer reviewing the query and passing it manually in [DB Browser for SQLite](https://sqlitebrowser.org/).
