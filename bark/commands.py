import sys
import re
import requests
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
    # def __init__(self, preserve_timestamp=False):
    #     self.preserve_timestamp = preserve_timestamp
        
    @classmethod
    def execute(cls, data, timestamp=None):
        utc_tz = timezone.utc
        # if not self.preserve_timestamp:
        
        data['date_added'] = timestamp or datetime.now(utc_tz).isoformat()
        db.add(
            'bookmarks',
            data
        )
        return "Bookmark added!"
    
# class ImportGithubStarsCommand:
    
#     @staticmethod
#     def _get_import_url(username):
#         return f'https://api.github.com/users/{username}/starred'
    
#     @staticmethod
#     def _get_next_import_url(links):
#         def split_string(link):
#             pattern = r'<([^>]+)>; rel="([^"]+)"'
#             groups = re.search(pattern, link)
#             url = None
#             rel = None
#             if groups:
#                 url = groups.group(1)
#                 rel = groups.group(2)
                
#             return url, rel
            
#         links = links.split(',')
#         for link in links:
#             url, rel = split_string(link)
#             if rel == 'next':
#                 return url
        
#         return None
        
#     @staticmethod
#     def _get_preserve_timestamp(preserve_timestamp):
#         return True if preserve_timestamp.upper() == 'Y' else False
    
#     @staticmethod
#     def _get_headers(preserve_timestamp=False):
#         headers = {
#             'X-GitHub-Api-Version': '2022-11-28'
#             }
#         if preserve_timestamp:
#             headers['Accept'] = 'application/vnd.github+json'
            
#         return headers
    
#     @staticmethod
#     def _get_bookmark_data(repo):
#         return {
#             'title': repo['name'],
#             'url': repo['url'],
#             'date_added': repo['created_at']
#         }
        
#     @staticmethod
#     def _create_bookmarks(bookmarks_data):
#         for bookmark in bookmarks_data:
#             _ = AddBookmarkCommand().execute(bookmark, bookmark['date_added'])
        
#         return f'Imported {len(bookmarks_data)} bookmarks from starred repos!'
    
#     @classmethod
#     def execute(cls, data):
#         url = cls._get_import_url(data['username'])
#         preserve_timestamp = cls._get_preserve_timestamp(data['preserve_timestamp'])
#         headers = cls._get_headers(preserve_timestamp)
#         bookmarks_data = []
#         while True:
#             response = requests.get(url=url, headers=headers)
#             if response.status_code == 200:
#                 repos = response.json()
#                 for repo in repos:
#                     bookmark = cls._get_bookmark_data(repo)
#                     bookmarks_data.append(bookmark)

#                 url = cls._get_next_import_url(response.headers['Link'])
#                 if not url:
#                     break
                
#         message = cls._create_bookmarks(bookmarks_data)
        
#         return message
            
class ImportGithubStarsCommand:
    @staticmethod
    def _extract_bookmark_info(repo):
        return {
            'title': repo['name'],
            'url': repo['html_url'],
            'notes': repo['description']
        }
        
    def execute(self, data):
        bookmarks_imported = 0
        
        github_username = data['github_username']
        next_page_of_results = f'https://api.github.com/users/{github_username}/starred'
        
        while next_page_of_results:
            starts_respose = requests.get(
                next_page_of_results,
                headers= {'Accept': 'application/vnd.github.v3.star+json'}
            )
            next_page_of_results = starts_respose.links.get('next', {}).get('url')
            
            for repo_info in starts_respose.json():
                repo = repo_info['repo']
                
                if data['preserve_timestamps']:
                    timestamp = datetime.strptime(
                        repo_info['starred_at'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                else:
                    timestamp = None
                    
                bookmarks_imported += 1
                AddBookmarkCommand.execute(
                    self._extract_bookmark_info(repo),
                    timestamp=timestamp
                )
        
        return f'Imported {bookmarks_imported} bookmarks from starred repos!'
        
        
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
    
class EditBookmarksCommand:
    @classmethod
    def execute(cls, data):
        criteria = {'id': data['bookmark_id']}
        del data['bookmark_id']
        db.update('bookmarks',
                  update_values = data,
                  criteria=criteria
                  )
        return 'Bookmark updated!'
    
class DeleteBookmarksCommand:
    @classmethod
    def execute(cls, bookmark_id):
        db.delete('bookmarks', {'id': bookmark_id})
        return 'Bookmark deleted!'
    
class QuitCommand:
    @classmethod
    def execute(cls):
        sys.exit()
        