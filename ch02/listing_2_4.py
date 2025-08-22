import random

OPTIONS = ['rock', 'paper', 'scissors']

def display_options():
    mesaage = '\n'.join(f'({i}) {option.title()}' for i, option in enumerate(OPTIONS, 1))
    print(mesaage)

def get_input_choice_from_user():
    try:
        choice_number = int(input('Enter the number of your choice: '))
        human_choice = OPTIONS[choice_number - 1]
        return human_choice
    except:
        return None
    
def get_human_choice():
    while True:
        human_choice = get_input_choice_from_user()
        if human_choice is not None:
            break
        
    print(f'You chose {human_choice}')
    return human_choice
       
def get_computer_choice():
    computer_choice = random.choice(OPTIONS)
    print(f'The computer chose {computer_choice}')
    return computer_choice

class RockScissorsPaperSimulator:
    WIN_RULES = {
    'rock': ['scissors'],
    'paper': ['rock'],
    'scissors': ['paper']
    }
    
    def __init__(self, human_choice, computer_choice):
        self.human_choice = human_choice
        self.computer_choice = computer_choice
        
    def apply_rules(self):
        if self.computer_choice == self.human_choice:
            print('Draw!')
            return
        
        if self.computer_choice in self.WIN_RULES[self.human_choice]:
            print(f'Yes, {self.human_choice} beat {self.computer_choice}!')
            return
        
        print(f'Sorry, {self.computer_choice} beat {self.human_choice}')
        return
    
    def __call__(self):
        self.apply_rules()
        

def main():
    display_options()
    game = RockScissorsPaperSimulator(
        human_choice=get_human_choice(),
        computer_choice=get_computer_choice()
        )
    game()
    
if __name__ == '__main__':
    main()