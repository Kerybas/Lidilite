import lidilite
import sqlite3

data = [
    {'id': 'A00001', 'color': 'blue', 'count': 3, 'size': 1.6, 'content': ['stuff1', 'stuff2']},
    {'id': 'A00002', 'color': 'red', 'count': 6, 'size': 2, 'content': []},
    {'id': 'A00003', 'count': 3, 'size': 1.6},
    {'id': 'A00004', 'color': 'green', 'count': 0, 'size': 7.4, 'content': ['stuff1', 'stuff2', 'stuff4']}
]

replace_data = [{"id": "A00001", "color": "dark blue", "count": 3, "size": 1.6, "content": "no more stuff"}]

valid_create_query = 'CREATE TABLE "TABLE_1" (\n' \
                    '\t"id"\tTEXT,\n' \
                    '\t"color"\tTEXT,' \
                    '\n\t"count"\tINTEGER,' \
                    '\n\t"size"\tREAL,' \
                    '\n\t"content"\tTEXT,' \
                    '\n\tPRIMARY KEY("id"));'

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute(valid_create_query)

valid_data_in_table = [('A00001', 'blue', 3, 1.6, "['stuff1', 'stuff2']"),
                       ('A00002', 'red', 6, 2.0, '[]'),
                       ('A00003', None, 3, 1.6, None),
                       ('A00004', 'green', 0, 7.4, "['stuff1', 'stuff2', 'stuff4']")]

valid_data_after_replace = [('A00002', 'red', 6, 2.0, '[]'),
                            ('A00003', None, 3, 1.6, None),
                            ('A00004', 'green', 0, 7.4, "['stuff1', 'stuff2', 'stuff4']"),
                            ('A00001', 'dark blue', 3, 1.6, 'no more stuff')]


def test_create_query():
    create_query = lidilite.draft_create_table(data, table_name='TABLE_1', mode='all', primary_keys='id')
    assert create_query == valid_create_query


def test_insert():
    table = lidilite.Table(conn, 'TABLE_1')
    table.insert(data)
    test_data_in_table = cur.execute('SELECT * FROM TABLE_1').fetchall()
    assert test_data_in_table == valid_data_in_table


def test_replace():
    table = lidilite.Table(conn, 'TABLE_1')
    table.replace(replace_data)
    test_data_after_replace = cur.execute('SELECT * FROM TABLE_1').fetchall()
    assert test_data_after_replace == valid_data_after_replace
