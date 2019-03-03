def draft_create_query(data, table_name='NEW_TABLE', mode='all'):
    all_keys, common_keys, uncommon_keys = find_keys(data)
    if mode == 'common':
        selected_keys = common_keys
    else:
        selected_keys = all_keys

    keys_types = give_keys_types(data, selected_keys)
    keys_sql_types = convert_to_sql_types(keys_types)
    query = prepare_query(table_name, keys_sql_types)

    return query


def find_keys(data):
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
    keys_types = {}
    for key in selected_keys:
        types = set()
        for data_row in data:
            try:
                vtype = give_val_type(data_row[key])
                types.add(vtype)
            except KeyError:
                pass

        keys_types[key] = types

    return keys_types


def convert_to_sql_types(keys_types):
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


def prepare_query(table_name, keys_sql_types):
    column_declarations = []
    for key, vtype in keys_sql_types.items():
        str_line = '\t"{}"\t{}'.format(key, vtype)
        column_declarations.append(str_line)

    column_declarations = ',\n'.join(column_declarations)

    query = 'CREATE TABLE "{}" (\n'.format(table_name) + column_declarations + ');'

    return query
