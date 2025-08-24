import sqlite3

class DatabaseManager:
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)
        
    def create_table(self, table_name, columns):
        columns = [f'{column} {data_type}' for column, data_type in columns.items()]
        columns = ', '.join(columns)
        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({columns});
            """
        )
        
    def add(self, table_name, columns_values):
        column_names = ', '.join(columns_values.keys())
             
        # placeholder = '? '*len(columns_values.keys())
        # placeholder = placeholder.strip().replace(' ', ', ')
        placeholder = ', '.join('?' * len(columns_values))
        
        columns_values = tuple(columns_values.values())
        self._execute(
            f"""
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholder});
            """,
            columns_values
        )
        
    def delete(self, table_name, criteria):
        # criteria = [f'{column} = {value}' for column, value in criteria]
        # if len(criteria) > 1:
        #     filter_criteria = []
        #     for n, el in enumerate(criteria):
        #         if n != len(criteria) - 1:
        #             el += ' AND '
        #         filter_criteria.append(el)
        # else:
        #     filter_criteria = criteria[0]
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            """,
            tuple(criteria.values())
        )
        
    def select(self, table_name, criteria=None, order_by=None):
        # placeholders = [f'{column} = ?' for column in criteria.keys()] if criteria else []
        # search_criteria = ' AND '.join(placeholders) if placeholders else ''
        # values = tuple(criteria.values()) if criteria else None
        
        # search_query = f"SELECT * FROM {table_name}"
        # if search_criteria:
        #     search_query += f"WHERE {search_criteria} ORDER BY {order_by};"
        # else:
        #     search_query += f"ORDER BY {order_by};"
            
        # self._execute(
        #     statement=search_query,
        #     values=values
        # )
        
        criteria = criteria or {}
        
        query = f"SELECT * FROM {table_name}"
        
        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f" WHERE {select_criteria}"
            
        if order_by:
            query += f" ORDER BY {order_by}"
            
        query += ";"
       
        return self._execute(
            query,
            tuple(criteria.values())
            )
        
    def __del__(self):
        self.connection.close()
        
    def _execute(self, statement, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor