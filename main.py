import shutil
import time
import random
import curses

class Tile: # Just tiles

    def __init__(self, coords, color=0, character = " ", transitable = True, behaviour = None):
        self.coords = coords
        self.character = character
        self.color = color
        self.transitable = transitable
        self.behaviour = behaviour
        self.nextone = self.coords

class Body(Tile): # Body of the snake

    def adjacent(self, coords):
        self.nextone = coords

class Head(Tile): # Head of the snake

    def start(self, limit = -1):
        self.start_coordinates = self.coords
        self.limit = limit
        self.trigered = False
        self.length = 0

    def run(self, handler): # Control method
        self.nextone = self.coords
        die = False
        coords = self.coords
        election = self.behaviour.choose(handler, self.coords)
        if election:
            self.move(election, handler)
        else:
            die = True
            self.die(handler)
        if self.length == self.limit and not self.trigered:
            handler.removing.append(self.start_coordinates)
            self.trigered = True
        self.length += 1
        return die # Returns if the head has died(so the cleaner can give it a proper burial)

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

class IA: # Seems like our snakes are becoming intelligent

    def __init__(self, variacion = [(0, 1), (0, -1), (1, 0), (-1, 0)], weight = [1, 1, 1, 1], 
                random_weight = True, crazy_behaviour = False, max_jump = 2):
        self.variacion = variacion
        self.weight = weight
        if random_weight:
            self.random_weight()
        if crazy_behaviour:
            self.crazy_behaviour(jump_limit=max_jump)

    def choose(self, mapa, coords): # Make a the decision of where to move on
        possibilities = []
        weight = []
        longitud = len(self.variacion)
        for x in range(0, longitud):
            coordinates = (self.variacion[x][0] + coords[0], self.variacion[x][1] + coords[1])
            tile = mapa.get_coords(coordinates)
            if tile != False and tile.transitable: # We check if the tile is free
                possibilities.append(coordinates)
                weight.append(self.weight[x])
        option = False
        if len(possibilities) > 0: # If there is a possible tile, we choose a random possible position
            option = self.weighted_choice(possibilities, weight)
        return option

    def weighted_choice(self, options, weight): # Make a decision, weighted based on the values of weight
        chooser = []
        counter = 0
        for x in weight:
            counter += x
            chooser.append(counter)
        eleccion = random.uniform(0, chooser[-1])
        for x in range(0, len(chooser)):
            if eleccion < chooser[x]:
                return options[x]

    def random_weight(self): # Generates a random weighted list
        total_weight = 0
        maximum_weigth = 1
        for x in range(0, len(self.weight)):
            weight = random.uniform(0.001, maximum_weigth)
            total_weight += weight
            self.weight[x] = weight

    def crazy_behaviour(self, jump_limit=2): # Just for some random fun
        for x in range(0, len(self.variacion)):
            self.variacion[x] = (random.randint(-jump_limit, jump_limit), random.randint(-jump_limit, jump_limit))

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

    def print_grid(self, stdscr): # Prints the map using the curses library
        for y in range(0, len(self.grid) - 1):
            y = self.grid[y]
            stdscr.addstr("\n")
            for x in y:
                stdscr.addstr(x.character, curses.color_pair(x.color))
        stdscr.addstr("\n")
        for x in self.grid[len(self.grid)-1]:
            stdscr.addstr(x.character, curses.color_pair(x.color))
        stdscr.refresh()
        stdscr.clear()

    def get_coords(self, coords): # Get the object at the given coords
        if coords[0] >= 0 and coords[1] >= 0:
            try:
                return self.grid[coords[1]][coords[0]]
            except IndexError:
                return False
        else:
            return False

    def set_coords(self, coords, objeto): # Set the object at the given coords
        try:
            self.grid[coords[1]][coords[0]] = objeto
        except IndexError:
            return False

class Handler(Mapa): # The snake charmer

    def __init__(self, alto, ancho, colors, percentage = 25, clean = True, dalton = False, headlimit = 1, max_length = -1, 
                random_weight = True, crazy_behaviour = False, max_jump = 2):
        self.alto =alto
        self.ancho = ancho
        self.percentage = percentage
        self.clear = clean
        self.dalton = dalton
        self.max_length = max_length
        self.random_weight = random_weight
        self.crazy_behaviour = crazy_behaviour
        self.max_jump = max_jump
        self.colors = colors
        self.grid = self.gen_grid()
        self.heads = {}
        self.removing = []
        self.head_limit = headlimit

    def run(self, gen = False): # Control method
        if gen:
            self.gen_head() # Gen the heads
        heads = list(self.heads.keys())
        for x in heads: # Updates the heads
            die = self.heads[x].run(self, x)
            if die:
                if not self.heads[x].trigered:
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
                    # And now, he would hit me 'cause a magician never show its tricks

    def gen_head(self): # Gens a new head
        if len(self.heads) != self.head_limit:
            if random.randint(0, 100) <= self.percentage:
                salir = False
                while not salir:
                    coords = (random.randint(0, self.ancho-1), random.randint(0, self.alto-1))
                    if self.get_coords(coords).transitable:
                        ia = IA(random_weight = self.random_weight, crazy_behaviour = self.crazy_behaviour, max_jump = self.max_jump)
                        self.heads[coords] = Head(coords, character="O", color = self.random_color(), transitable = False, behaviour = ia)
                        self.heads[coords].start(limit = self.max_length)
                        self.set_coords(coords, self.heads[coords])
                        salir = True
    
    def random_color(self): # Returns a random color
        if not self.dalton:
            return random.choice(self.colors)
        else:
            return 8

def read_config(arch="./config.conf"): # Reads config
    returneo = {}
    with open(arch) as f:
        for x in f.readlines():
            x = x.replace(" ", "")
            x = x.replace("\t", "")
            if x[0]!="#" and "=" in x and x != "\n":
                linea = x.split("=")
                returneo[linea[0]] = linea[1].replace("\n", "")
    return returneo

def main(stdscr): # The root method, do not annoy him
    size = shutil.get_terminal_size()
    config = read_config()
    true = ["True", "true", "TRUE", "1"]
    curses.start_color()
    curses.use_default_colors()
    colors = []
    for i in range(0, curses.COLORS):
        curses.init_pair(i+1, i, -1)
        colors.append(i)
    mapa = Handler(size[1]-1, size[0]-1, colors,clean = config["clear"] in true, percentage = int(config["percentage"]), 
        dalton = config["daltonism"] in true, max_length = int(config["max_length"]), headlimit = int(config["limit"]),
        random_weight = config["random_weighted"] in true, crazy_behaviour = config["crazy"] in true)
    while True:    
        mapa.run(gen=True)
        mapa.print_grid(stdscr)
        time.sleep(1/int(config["fps"]))

curses.wrapper(main)

