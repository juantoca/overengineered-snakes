import shutil
import time
import random

class Tile: # Just tiles

    def __init__(self, coords, color="0;30;40", character = "█", transitable = True):
        self.coords = coords
        self.character = character
        self.color = color
        self.transitable = transitable

    def printeo(self): # Returns the text to be printed on the tile position
        return "\x1b[" + self.color + "m" + self.character + "\x1b[0m"

class Body(Tile): # Body of the snake

    def adjacent(self, coords):
        self.nextone = coords

class Head(Tile): # Head of the snake

    def start(self):
        self.start_coordinates = self.coords

    def run(self, handler): # Control method
        die = False
        coords = self.coords
        election = self.choose(handler)
        if election:
            self.move(election, handler)
        else:
            die = True
            self.die(mapa)
        return die # Returns if the head has died(so the cleaner can give it a proper burial)


    def choose(self, mapa): # Choose the next tile to move on
        variacion = ((0, 1), (0, -1), (1, 0), (-1, 0))
        possibilities = []
        for x in variacion:
            coords = (self.coords[0] + x[0], self.coords[1] + x[1])
            tile = mapa.get_coords(coords)
            if tile != False and tile.transitable: # We check if the tile is free
                possibilities.append(coords)
        option = False
        if len(possibilities) > 0: # If there is a possible tile, we choose a random possible position
            option = random.choice(possibilities)
        return option

    def move(self, coords, mapa): # Moves the head to the given coords
        mapa.set_coords(self.coords, Body(self.coords, color = self.color, character = "#", transitable = False)) # We create a body part on previous location
        tile = mapa.get_coords(self.coords)
        tile.adjacent(coords) # And we set the nextone attribute of the body to the position where we are moving to
        self.coords = coords
        mapa.set_coords(coords, self) # Finally, we change the destination tile to ourselfs

    def die(self, mapa): # Kil... I mean, sends the head to its bedroom and sets a body on it's position
        mapa.set_coords(self.coords, Body(self.coords, color = self.color, character = "#", transitable = False)) # Changes the tile
        tile = mapa.get_coords(self.coords)
        tile.adjacent(self.coords) # Sets the nextone attribute to itself(so the cleaner knows the snake ends)

class Mapa: # Map management

    def __init__(self, alto, ancho):
        self.alto = alto
        self.ancho = ancho
        self.grid = self.gen_grid()

    def gen_grid(self): # Generates the grid, filing it with empty tiles
        returneo = []
        for y in range(0, self.alto):
            returneo.append([])
            for x in range(0, self.ancho):
                returneo[y].append(Tile((x, y)))
        return returneo

    def print_grid(self): # Returns the text to be printed
        mapa = ""
        for y in self.grid:
            mapa += "\n"
            for x in y:
                mapa += x.printeo() 
        return mapa

    def get_coords(self, coords): # Get the object at the given coords
        try:
            return self.grid[coords[1]][coords[0]]
        except IndexError:
            return False

    def set_coords(self, coords, objeto): # Set the object at the given coords
        try:
            self.grid[coords[1]][coords[0]] = objeto
        except IndexError:
            return False

class Handler(Mapa): # The snake charmer

    def __init__(self, alto, ancho, percentage = 25, clean = True, dalton = False):
        self.alto =alto
        self.ancho = ancho
        self.percentage = percentage
        self.clear = clean
        self.dalton = dalton
        self.grid = self.gen_grid()
        self.heads = {}
        self.removing = []
    
    def run(self, gen = False): # Control method
        if gen:
            self.gen_head() # Gen the heads
        heads = list(self.heads.keys())
        for x in heads: # Updates the heads
            die = self.heads[x].run(self)
            if die:
                self.removing.append(self.heads[x].start_coordinates) # We set that there's a new snake that needs a meatgrinder session
                del self.heads[x]
        if self.clear:
            self.clean() # Do some magic, just don't touch it

    def clean(self): # Harry Potter would be proud of this method
        remove = [] # We store the coords of the snakes that has been deleted completly
        for x in range(0, len(self.removing)):
            coords = self.removing[x]
            tile = self.get_coords(coords)
            nexts = tile.nextone # We store the next position of the snake
            self.removing[x] = nexts
            if nexts == coords: # This means that it was the last position so we delete it from erasing list
                remove.append(coords)
            self.set_coords(coords, Tile(coords)) # Finally, we clean the tile
        for x in remove:
            self.removing.remove(x)
                    # And now, he would hit me cause a magician never show its tricks

    def gen_head(self): # Gens a new head
        if random.randint(0, 100) <= self.percentage:
            salir = False
            while not salir:
                coords = (random.randint(0, self.ancho-1), random.randint(0, self.alto-1))
                if self.get_coords(coords).transitable:
                    self.heads[coords] = Head(coords, character="O", color = self.random_color(), transitable = False)
                    self.heads[coords].start()
                    self.set_coords(coords, self.heads[coords])
                    salir = True
    
    def random_color(self): # Returns a random color
        colors = ["31", "32", "33", "34", "35", "36", "37"]
        if not self.dalton:
            return "0;"+random.choice(colors)+";40"
        else:
            return "0;32;40"

def read_config(arch="./config.conf"): # Reads config
    returneo = {}
    with open(arch) as f:
        for x in f.readlines():
            if x[0]!="#" and "=" in x:
                x = x.replace(" ", "")
                linea = x.split("=")
                returneo[linea[0]] = linea[1].replace("\n", "")
    return returneo

size = shutil.get_terminal_size()
config = read_config()
true = ["True", "true", "TRUE", "1"]
mapa = Handler(size[1], size[0], clean = config["clear"] in true, percentage = int(config["percentage"]), dalton = config["daltonism"] in true)
while True:
    mapa.run(gen = True)
    print(mapa.print_grid())
    time.sleep(1/int(config["fps"]))

