# Shoddy procedural code
import random

OPTIONS = ['rock', 'paper', 'scissors', 'Spock', 'lizard']
WIN_RULES = {
    'rock': ['scissors', 'lizard'],
    'paper': ['rock', 'Spock'],
    'scissors': ['paper', 'lizard'],
    'Spock': ['scissors', 'rock'],
    'lizard': ['Spock', 'paper']
}

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

def apply_rules(human_choice, computer_choice):
    if computer_choice == human_choice:
        print('Draw!')
        return
    
    if computer_choice in WIN_RULES[human_choice]:
        print(f'Yes, {human_choice} beat {computer_choice}!')
        return
    
    print(f'Sorry, {computer_choice} beat {human_choice}')
    return
    
def main():
    display_options()
    human_choice = get_human_choice()
    computer_choice = get_computer_choice()
    apply_rules(
        human_choice,
        computer_choice
    )

if __name__ == '__main__':
    main()