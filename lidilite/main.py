class Table:
    """Object representing a sqlite3 table"""
    def __init__(self, connexion, table):
        self.cnx = connexion
        self.table = table
        self.columns = self.get_columns()

    def get_columns(self):
        """
            Get columns' name and type from the sqlite table.
            return a list of tuples (column_name, type).
            Example:
            [('id', 'TEXT'),
             ('color', 'TEXT'),
             ('count', 'INTEGER'),]
        """
        columns = []
        with self.cnx as cnx:
            for col_info in cnx.execute("pragma table_info('{}');".format(self.table)):
                columns.append((col_info[1], col_info[2]))
        return columns

    def _datarow_to_sqldict(self, data_dict):
        """
            Prepare the content of a dictionary, to be loaded in the table.
            Select only the keys present in the table and provide empty values for keys
            in the table but absent from the dictionary.
            Force the value types to match the table types.
        Args:
            data_dict: a dictionary from the data list of dicts.

        Returns:
            sql_dict: a dictionary matching columns and types of the table.

        """
        sql_dict = {}
        for column_name, column_type in self.columns:
            try:
                val = data_dict[column_name]
            except KeyError:
                val = None

            if val != None: # '!= None' needed to differentiate None from [].
                if column_type == 'INTEGER':
                    val = int(val)
                elif column_type == 'REAL':
                    val = float(val)
                elif column_type == 'TEXT':
                    val = str(val)
                else:
                    val = str(val)

            sql_dict[column_name] = val
        return sql_dict

    def _build_query(self, sql_dict, mode):
        """
            Build the INSERT or REPLACE query, using the sql_dict to populate the sql_values.
        Args:
            sql_dict: dictionary prepared by _datarow_to_sqldict()
            mode: sqlite3 loading behavior, either 'REPLACE' or 'INSERT'

        Returns:
            sql_query, sql_values :
                sql_query is a string like:
                'REPLACE INTO NEW_TABLE(id,color,count,size,content) VALUES(?,?,?,?,?)'
                sql_values is a list of values, to be passed through the '?'.
        """
        columns_names = [column[0] for column in self.columns]
        sql_holders = ','.join('?' * len(sql_dict))
        sql_columns = ','.join(columns_names)
        sql_values = [sql_dict[col] for col in columns_names]

        if mode in ('INSERT', 'REPLACE'):
            sql_query = '{} INTO {}({}) VALUES({})'.format(mode, self.table, sql_columns, sql_holders)
        else:
            raise ValueError('{} is not a valid mode.'.format(mode))

        self._sql_query = sql_query
        self._sql_values = sql_values

        return sql_query, sql_values

    def load(self, data_list_dicts, mode):
        """
        Wrap the sql dict creation, query writing and query execution, for any dictionary
        in a list of dictionaries.
        Args:
            data_list_dicts: a list of dictionaries to be loaded in the table.
            mode: sqlite3 loading behavior, either 'REPLACE' or 'INSERT'
        """
        with self.cnx as cnx:
            cursor = cnx.cursor()
            for data_dict in data_list_dicts:
                sql_dict = self._datarow_to_sqldict(data_dict)
                sql_query, sql_values = self._build_query(sql_dict, mode)
                cursor.execute(sql_query, sql_values)

    def insert(self, data_list_dicts):
        """Shortcut to load in INSERT mode"""
        self.load(data_list_dicts, mode='INSERT')

    def replace(self, data_list_dicts):
        """Shortcut to load in REPLACE mode"""
        self.load(data_list_dicts, mode='REPLACE')

    def insert_or_replace(self, data_list_dicts):
        """
        Shortcut to load in REPLACE mode.
        In Sqlite3 there is no difference between REPLACE and INSERT OR REPLACE.
        """
        self.load(data_list_dicts, mode='REPLACE')
