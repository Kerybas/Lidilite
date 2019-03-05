def draft_create_table(data, table_name='NEW_TABLE', mode='all', primary_keys=None):
    """
        This function takes a dataset (list of dicts) and returns a string representing
        a SQLite CREATE TABLE query, matching the dataset structure.

    :param data: (list of dicts) the dataset you plan to insert in a SQLite table.
    :param table_name: (str) the name of your SQLite table
    :param mode: (str) either 'all' or 'common'.
                 - 'all': create a table including all possible columns found in the dataset.
                    If a key appears at least one time in the list of dicts, it will generate a column.
                 - 'common': create a table including only columns that are found in every dictionary.
                   If a key appears only in a few dicts, it will not generate a column.
    :param primary_keys: (str, list, or None) either a single primary key, a list of primary keys, or nothing.

    :return: (str) a SQLite CREATE TABLE query.
    """
    all_keys, common_keys, uncommon_keys = find_keys(data)
    if mode == 'common':
        selected_keys = common_keys
    else:
        selected_keys = all_keys

    keys_types = give_keys_types(data, selected_keys)
    keys_sql_types = convert_to_sql_types(keys_types)
    query = prepare_query(table_name, keys_sql_types, primary_keys)

    return query


def find_keys(data):
    """
        Find the keys in the dictionaries of a list of dicts.

    :param data: (list of dicts) a dataset
    :return: (tuple of three lists) all_keys, common_keys, uncommon_keys:
             - all_keys: all unique keys found at least once across the dataset.
             - common_keys: unique keys commonly found in every dicts.
             - uncommon_keys: uniques keys found in some dicts but not all.
    """
    uncommon_keys = []

    all_keys = list(data[0].keys())

    for data_row in data:
        row_keys = data_row.keys()
        for row_key in row_keys:
            if row_key not in all_keys:
                all_keys.append(row_key)
                uncommon_keys.append(row_key)
        for all_key in all_keys:
            if all_key not in row_keys:
                uncommon_keys.append(all_key)

    common_keys = [key for key in all_keys if key not in uncommon_keys]

    return all_keys, common_keys, uncommon_keys


def give_val_type(val):
    """Evaluate if a variable is a boolean, a string, an integer, a float or other."""
    if isinstance(val, bool):
        vtype = 'boolean'
    elif isinstance(val, str):
        vtype = 'string'
    elif isinstance(val, int):
        vtype = 'int'
    elif isinstance(val, float):
        vtype = 'float'
    else:
        vtype = 'other'

    return vtype


def give_keys_types(data, selected_keys):
    """
        Evaluate the type(s) of each key in the dataset, for a selected list of keys.

    :param data: (list of dicts) a dataset
    :param selected_keys: (list) a list of keys to analyse
    :return: (dict) a dictionary of key and a set of unique types found for that key.
             Example: {'col1': {'string'}, 'col2': {'int','float'}}
    """
    keys_types = {}
    for key in selected_keys:
        types = set()
        for data_dict in data:
            try:
                vtype = give_val_type(data_dict[key])
                types.add(vtype)
            except KeyError:
                pass

        keys_types[key] = types

    return keys_types


def convert_to_sql_types(keys_types):
    """
        Take the dict of unique types from give_keys_types, select the best type if
        multiple types found, and return a dict of key:sql_type.

    :param keys_types: (dict) a dictionary of key and a set of unique types found for that key.
    :return: (dict) a dictionary of key and SQLite type.
             Example: {'col1': 'TEXT', 'col2': 'REAL'}
    """
    keys_sql_types = {}
    for key, types in keys_types.items():
        if len(types) > 1 and types != {'int', 'float'}:
            sql_type = 'TEXT'
        elif types == {'int', 'float'} or types == {'float'}:
            sql_type = 'REAL'
        elif types == {'int'} or types == {'boolean'}:
            sql_type = 'INTEGER'
        else:
            sql_type = 'TEXT'

        keys_sql_types[key] = sql_type

    return keys_sql_types


def prepare_query(table_name, keys_sql_types, primary_keys=None):
    """
    Wrap the table name, SQLite types and primary key(s) in a SQLite query.
    Args:
        table_name: (str) the name of your SQLite table
        keys_sql_types: (dict) a dictionary of key and SQLite type.
        primary_keys: (str, list, or None) either a single primary key, a list of primary keys, or nothing.

    Returns:(str) a SQLite CREATE TABLE query.

    """
    column_declarations = []
    for key, vtype in keys_sql_types.items():
        str_line = '\t"{}"\t{}'.format(key, vtype)
        column_declarations.append(str_line)

    table_declarations = 'CREATE TABLE "{}" (\n'.format(table_name)
    column_declarations = ',\n'.join(column_declarations)
    if primary_keys:

        if not isinstance(primary_keys, list):  # if only one key is passed, not in a list
            primary_keys = [primary_keys]

        primary_keys = ['"{}"'.format(key) for key in primary_keys]
        primary_keys_declaration = ',\n\tPRIMARY KEY(' + ','.join(primary_keys) + ')'
    else:
        primary_keys_declaration = ''

    query = table_declarations + column_declarations + primary_keys_declaration + ');'

    return query
