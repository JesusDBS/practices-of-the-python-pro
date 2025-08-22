import datetime

def day():
    return datetime.datetime.now().strftime('%A')

def part_of_day():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return 'morning'
    elif hour < 18:
        return 'afternoon'
    else:
        return 'evening'

class Greeter:
    def greet(self, store: str):
        print(f"""
              Hi, welcome to {store}!
              Hows your {day()} {part_of_day()} going?
              Here's a coupon  for 20% off!!
              """)
        
def main():
    greeter = Greeter()
    greeter.greet('The Python Store')
    
if __name__ == '__main__':
    main()