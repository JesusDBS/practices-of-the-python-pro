class Tire:  # <1>
    def __repr__(self):
        return 'A rubber tire'
    
class SlimTire:
    def __repr__(self):
        return 'A slim tire'


class Frame:
    def __repr__(self):
        return 'An aluminum frame'

#listing 7.6
class CarbonFiberFrame:
    def __repr__(self):
        return 'A carbon frame'
    

class Bicycle:
    def __init__(self, front_tire, back_tire, frame):
        self.front_tire = front_tire
        self.back_tire = back_tire
        self.frame = frame
        
    def print_specs(self):  # <3>
        print(f'Frame: {self.frame}')
        print(f'Front tire: {self.front_tire}, back tire: {self.back_tire}')
        
if __name__ == "__main__":
    bike = Bicycle(
        # front_tire=Tire(),
        front_tire=SlimTire(),
        back_tire=Tire(),
        # frame=Frame()
        frame=CarbonFiberFrame()
    )
    bike.print_specs()