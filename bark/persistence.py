from abc import ABC, abstractmethod

from database import DatabaseManager

class PersistenceLayer(ABC):
    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def list(self, order_by):
        raise NotImplementedError

    @abstractmethod
    def edit(self, bookmark_id, data):
        raise NotImplementedError

    @abstractmethod
    def delete(self, bookmark_id):
        raise NotImplementedError
    
class BookmarksDatabase(PersistenceLayer):
    def __init__(self):
        self.db = DatabaseManager('bookmarks.db')
        self._table_name = 'bookmarks'
        columns = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'title': 'TEXT NOT NULL',
            'url': 'TEXT NOT NULL',
            'notes': 'TEXT',
            'date_added': 'TEXT NOT NULL'
        }
        self.db.create_table(
            self._table_name,
            columns
        )
        
    def create(self, data):
        self.db.add(
            self._table_name,
            columns_values=data
        )
        
    def list(self, order_by):
        return self.db.select(
            self._table_name,
            order_by=order_by
        )
        
    def edit(self, bookmark_id, data):
        self.db.update(
            self._table_name,
            criteria=bookmark_id,
            update_values=data,
        )
        
    def delete(self, bookmark_id):
        self.db.delete(
            self._table_name,
            criteria=bookmark_id
        )
        
    
        

