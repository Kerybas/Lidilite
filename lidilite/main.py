class Table:
    def __init__(self, connexion, table):
        self.cnx = connexion
        self.table = table
        self.columns = self.get_columns()

    def get_columns(self):
        columns = []
        with self.cnx as cnx:
            for col_info in cnx.execute("pragma table_info('{}');".format(self.table)):
                columns.append((col_info[1], col_info[2]))
        return columns

    def _datarow_to_sqldict(self, data_row):
        sql_dict = {}
        for column_name, column_type in self.columns:
            try:
                val = data_row[column_name]
            except KeyError:
                val = None

            if val != None:
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

    def _prep_query(self, data_row, mode):
        columns_names = [column[0] for column in self.columns]
        sql_dict = self._datarow_to_sqldict(data_row)
        sql_holders = ','.join('?' * len(sql_dict))
        sql_columns = ','.join(columns_names)
        sql_values = [sql_dict[col] for col in columns_names]

        if mode in ('INSERT', 'INSERT OR REPLACE', 'REPLACE'):
            sql_query = '{} INTO {}({}) VALUES({})'.format(mode, self.table, sql_columns, sql_holders)
        else:
            raise ValueError('{} is not a valid mode.'.format(mode))

        self._sql_query = sql_query
        self._sql_values = sql_values

        return sql_query, sql_values

    def load(self, data, mode):
        with self.cnx as cnx:
            cursor = cnx.cursor()
            for data_row in data:
                sql_query, sql_values = self._prep_query(data_row, mode)
                cursor.execute(sql_query, sql_values)

    def insert(self, data):
        self.load(data, mode='INSERT')

    def replace(self, data):
        self.load(data, mode='REPLACE')

    def insert_or_replace(self, data):
        self.load(data, mode='INSERT OR REPLACE')
