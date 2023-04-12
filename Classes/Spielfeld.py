class Spielfeld:
    def __init__(self, bot = False):
        self.__hitfield = [[0] * 10] * 10
        self.__boatfield = [[0] * 10] * 10
        
        self.__bot = bot
        self.__ships = 10

    def show_boatfield(self):
        for l in self.__boatfield:
            for r in l:
                print(r, end="") 
            print("")

    def show_hitfield(self):
        for l in self.__hitfield:
            for r in l:
                print(r, end="") 
            print("")    

    def get_ships(self):
        return self.__ships
    
    def get_bot(self):
        return self.__bot
    
    def get_boatfield(self):
        return self.__boatfield

    def get_hitfield(self):
        return self.__hitfield

    def set_ship(self, shiplength):
        # ask startlocation and direction via arrows
        # check not over field size and not already set
        pass

if __name__ == "__main__":
    s1 = Spielfeld(True)
    s1.show_boatfield()