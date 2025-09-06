import os 
import commands

def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)

def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
        
def option_choice_is_valid(choice, options):
    return choice.upper() in options
        
def get_option_choice(options):
    choice = input('Choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice!')
        choice = input('Choose an option: ')
    return options[choice.upper()]

def get_user_input(input_name, required=True):
    while True:
        user_input = input(f'{input_name}: ')
        if not user_input and required:
            print(f'{input_name} is required!')
        else:
            break
    
    return user_input
    
def get_add_bookmark_data():
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', False)
    }
    
def get_delete_bookmark_data():
    return get_user_input('Bookmark ID')

# def get_import_github_starts_data():
#     return {
#         'username': get_user_input('Github username: '),
#         'preserve_timestamp': get_user_input('Preserve timestamps [Y/n]: ')
#     }

def github_import_options():
    return {
        'github_username': get_user_input('Github username'),
        'preserve_timestamps': 
            get_user_input(
                'Preserve timestamps [Y/n]',
                required=False
            ) in {'Y', 'y', None}
    }

class Option:
    def __init__(self, display_name, command, prep_step=None):
        self.display_name = display_name
        self.command = command
        self.prep_step = prep_step
        
    def choose(self):
        data = self.prep_step() if self.prep_step else None
        message = self.command.execute(data) if data else\
            self.command.execute()
        print(message)
        
    # def __call__(self):
    #     data = None
    #     if self.prep_step:
    #         data = self.prep_step()
        # if data:
    #       message = self.command.execute(data)
        # else:
        #     message = self.command.execute()
    #     print(message)
        
    def __str__(self):  
        return self.display_name
    
def main():
    while True:
        options = {
            'A': Option('Add a bookmark', commands.AddBookmarkCommand, get_add_bookmark_data),
            'B': Option('List bookmarks by date', commands.ListBookmarksCommand()), 
            'T': Option('List bookmarks by title', commands.ListBookmarksCommand('title')),
            'D': Option('Delete a bookmark', commands.DeleteBookmarksCommand, get_delete_bookmark_data),
            'G': Option('Import GitHub starts', commands.ImportGithubStarsCommand(), github_import_options),
            'Q': Option('Quit', commands.QuitCommand)
        }
        clear_screen()
        print_options(options)
        chosen_option = get_option_choice(options)
        clear_screen()
        chosen_option.choose()
        _ = input('Press ENTER to return to menu')

if __name__ == '__main__':
    commands.CreateBookmarksTableCommand.execute()
    main()