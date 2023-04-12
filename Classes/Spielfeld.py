from string import ascii_uppercase
from random import randint

class Spielfeld:
    def __init__(self, bot = False):
        self.__fsize = 10 
        self.__hitfield = [[0] * self.__fsize] * self.__fsize
        self.__boatfield = [[0] * self.__fsize] * self.__fsize
        
        self.__bot = bot
        self.__ships = 10

    # Print Field with Postion Indictaros at the top and left, like A1, B10, etc to the Command-Line
    def show_field(self, fieldtype):
        

        print(" " * (len(str(self.__fsize))+2), end = "")
        for a in range(self.__fsize):
            print(f"{ascii_uppercase[a]}", end = " ")
        print("\n")

        for num, l in enumerate(fieldtype, 1):
            print(f"{num}", end="   ")

            if(len(str(num)) > 1):
                print("\b"*(len(str(num))-1), end = "")

            for r in l:
                print(r, end=" ") 
            print("")

    def show_boatfield(self):
        self.show_field(self.__boatfield)

    def show_hitfield(self):
        self.show_field(self.__hitfield)

    # getter
    def get_ships(self):
        return self.__ships
    
    def get_bot(self):
        return self.__bot
    
    def get_boatfield(self):
        return self.__boatfield

    def get_hitfield(self):
        return self.__hitfield

    # setter
    def set_ship(self, shiplength):
        # ask startlocation and direction via arrows
        # check not over field size and not already set
        pass

if __name__ == "__main__":
    s1 = Spielfeld(True)
    s1.show_boatfield()