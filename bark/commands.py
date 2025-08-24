import sys
from datetime import datetime, timezone

from database import DatabaseManager

db = DatabaseManager('bookmarks.db')

class CreateBookmarksTableCommand:
    @classmethod
    def execute(cls):
        columns = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title': 'TEXT NOT NULL',
            'url': 'TEXT NOT NULL',
            'notes': 'TEXT',
            'date_added': 'TEXT NOT NULL'
        }
        db.create_table(
            'bookmarks',
            columns
        )
        
class AddBookmarkCommand:
    @classmethod
    def execute(cls, data):
        utc_tz = timezone.utc
        data['date_added'] = datetime.now(utc_tz).isoformat()
        db.add(
            'bookmarks',
            data
        )
        return "Bookmark added!"
    
class ListBookmarksCommand:
    def __init__(self, order_by='date_added'):
        self.order_by = order_by
        
    def execute(self):
        # self.order_by = order_by
        res = db.select(
            'bookmarks',
            order_by=self.order_by
            )
        return res.fetchall()
    
class DeleteBookmarksCommand:
    @classmethod
    def execute(cls, bookmark_id):
        db.delete('bookmarks', {'id': bookmark_id})
        return 'Bookmark deleted!'
    
class QuitCommand:
    @classmethod
    def execute(cls):
        sys.exit()
        