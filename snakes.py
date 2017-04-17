#! /usr/bin/env python

import shutil
import random
import curses
import signal


class Tile:  # Just tiles

    """
    Super-class that represents the basic information for an object of the grid
    """

    def __init__(self, coords, color=0, character=" ", transitable=True):
        """
        Constructor for the tile object
        :param coords: Initial coords of the object (x, y)
        :param color: Color of the object
        :param character: Character which will represent the object
        :param transitable: Self-explanatory
        """
        self.coords = coords
        self.character = character
        self.color = color
        self.transitable = transitable
        self.nextone = coords


class Body(Tile):  # Body of the snake

    """
    Class that represents a body tile of an snake
    """

    def __init__(self, coords, nextone, color=0, character="#", transitable=True):
        super().__init__(coords, color, character, transitable)
        self.nextone = nextone


class Head(Tile):  # Head of the snake

    """
    Class that represents the head of the snake. It does all the magic stuff
    """

    def __init__(self, coords, behaviour, color=0, character="0", transitable=True, limit=-1, body_char = "#"):
        """
        Constructor for the head class
        :param coords: Initial coords
        :param color: Color of the snake
        :param character: Character to represent the head
        :param transitable: Is it overwritable?
        :param behaviour: IA for the snake
        :param limit: Length limit for the snake
        """
        super().__init__(coords, color=color, character=character, transitable=transitable)
        self.behaviour = behaviour
        self.start_coordinates = self.coords
        self.limit = limit
        self.trigered = False
        self.length = 0
        self.body_char = body_char
        self.nextone = self.coords

    def run(self, handler):
        """
        Method to update the status of the snake
        :param handler: Game class to modify
        :return: True if the head has died
        """
        self.nextone = self.coords
        die = False
        election = self.behaviour.choose(handler, self.coords)  # We choose where to move
        if election:
            self.move(election, handler)  # If there is a possible tile, we move to the selected one
        else:
            die = True  # If not, we kill it
            self.die(handler)
        if self.length == self.limit \
                and not self.trigered:  # We add the snake to the cleaner in case it has reached the length limit
            handler.removing.append(self.start_coordinates)
            self.trigered = True
        self.length += 1
        return die  # Returns if the head has died(so the cleaner can give it a proper burial)

    def move(self, coords, mapa):
        """
        Moves the head
        :param coords: Coords to move to
        :param mapa: Game class to modify
        :return: VOID
        """
        mapa.set_coords(self.coords, Body(self.coords, coords, color=self.color, character=self.body_char,
                                          transitable=False))  # We create a body part on previous location
        self.coords = coords
        mapa.set_coords(coords, self)  # Finally, we change the destination tile to ourselfs

    def die(self, mapa):
        """
        Kills the snake
        :param mapa: Game class to modify
        :return: VOID
        """
        mapa.set_coords(self.coords, Body(self.coords, self.coords, color=self.color, character=self.body_char,
                                          transitable=False))  # Changes the tile


class IA:  # Seems like our snakes are becoming intelligent

    def __init__(self, variacion=[(0, 1), (0, -1), (1, 0), (-1, 0)], weight=[1, 1, 1, 1],
                 random_weight=True, crazy_behaviour=False, max_jump=2):
        """
        IA for the snakes
        :param variacion: Tuple of possible variations of the current position
        :param weight: Probability weights of the variations
        :param random_weight: Shall I generate random weights?
        :param crazy_behaviour: Shall I generate random variations?
        :param max_jump: If crazy_behaviour, Which is the maximum variation in both axes?
        """
        self.variacion = variacion
        self.weight = weight
        if random_weight:
            self.random_weight()
        if crazy_behaviour:
            self.crazy_behaviour(jump_limit=max_jump)

    def posible_moves(self, mapa, coords):
        """
        Checks which of the variation-appointed tiles are available to move to
        :param mapa: Game class to check in
        :param coords: Current coords
        :return: Tuple of tuples = (possibilities, weights)
        """
        possibilities = []  # Coordinates
        weight = []  # Weights
        longitud = len(self.variacion)
        for x in range(0, longitud):
            coordinates = (self.variacion[x][0] + coords[0], self.variacion[x][1] + coords[1])
            tile = mapa.get_coords(coordinates)
            if tile and tile.transitable:  # We check if the tile is free
                possibilities.append(coordinates)
                weight.append(self.weight[x])
        return possibilities, weight

    def choose(self, mapa, coords):
        """
        Chooses where the snake should move
        :param mapa: Game class to use
        :param coords: Current coordinates
        :return: Coordinates or False if not valid destination
        """
        possibilities = self.posible_moves(mapa, coords)
        possibilities = self.modify_weights(possibilities[0], possibilities[1], mapa)
        option = False
        if len(possibilities[0]) > 0:  # If there is a possible tile, we choose a random-weighted possible position
            option = self.weighted_choice(possibilities[0], possibilities[1])
        return option

    def modify_weights(self, possibilities, weight, mapa):
        """
        Checks the enviroment and modify the weights to make the best choice
        :param possibilities: Posible options
        :param weight: Weights of the options
        :param mapa: Game class
        :return: (possibilities, weights)
        """
        weighted = []
        for x in range(0, len(possibilities)):
            coords = possibilities[x]
            adjacents = 0
            for y in self.variacion:  # We count the number of bodys around a given possibility
                coordinates = (y[0] + coords[0], y[1] + coords[1])
                tile = mapa.get_coords(coordinates)
                if tile and tile.__class__.__name__ == "Body":
                    adjacents += 1
            if adjacents == 0:  # In case of no adjacency, we give privileges to the option
                weighted.append(weight[x] * 100)
            elif adjacents == 3:  # If it would die in the next cicle, we set the minimum weight
                weighted.append(0.001)
            else:  # If not, we give less priority based on the number of adjacent tiles
                weighted.append(weight[x] / adjacents)
        return possibilities, weighted

    def weighted_choice(self, options, weight):
        """
        Makes a choice based on the weights
        :param options: Possibilities to choose from
        :param weight: Weights of the possibilities
        :return: options element choosen
        """
        chooser = []
        counter = 0
        for x in weight:
            counter += x
            chooser.append(counter)
        eleccion = random.uniform(0, chooser[-1])  # We generate a random number between 0 and the sum of the weights
        for x in range(0, len(chooser)):
            if eleccion < chooser[x]:
                return options[x]

    def random_weight(self):
        """
        Generates random weights
        :return: VOID
        """
        total_weight = 0
        maximum_weigth = 1
        for x in range(0, len(self.weight)):
            weight = random.uniform(0.001, maximum_weigth)
            total_weight += weight
            self.weight[x] = weight

    def crazy_behaviour(self, jump_limit=2):
        """
        Generates random variations
        :param jump_limit: Limit of variation on both axes
        :return: VOID
        """
        for x in range(0, len(self.variacion)):
            self.variacion[x] = (random.randint(-jump_limit, jump_limit), random.randint(-jump_limit, jump_limit))


class Mapa:
    def __init__(self, alto, ancho):
        """
        Constructor class for the map
        :param alto: height
        :param ancho: width
        """
        self.alto = alto
        self.ancho = ancho
        self.grid = self.gen_grid()

    def gen_grid(self):
        """
        Generates the grid matrix, filing it with empty tiles
        :return: Matrix map
        """
        returneo = []
        for y in range(0, self.alto):
            returneo.append([])
            for x in range(0, self.ancho):
                returneo[y].append(Tile((x, y)))
        return returneo

    def print_grid(self, stdscr):
        """
        Prints the map using the curses library
        :param stdscr: Stdscr object from curses library
        :return: VOID
        """
        stdscr.clear()
        for y in range(0, len(self.grid) - 1):
            y = self.grid[y]
            stdscr.addstr("\n")
            for x in y:
                stdscr.addstr(x.character, curses.color_pair(x.color))
        stdscr.addstr("\n")
        for x in self.grid[len(self.grid) - 1]:
            stdscr.addstr(x.character, curses.color_pair(x.color))
        stdscr.refresh()

    def get_coords(self, coords):
        """
        Return the object at given coords
        :param coords: Coordinates to search in
        :return: (x, y) or False if not a valid tile
        """
        if coords[0] >= 0 and coords[1] >= 0:
            try:
                return self.grid[coords[1]][coords[0]]
            except IndexError:
                return False
        else:
            return False

    def set_coords(self, coords, objeto):
        """
        Changes the object at given coords
        :param coords: Coordinates to change
        :param objeto: Object to insert
        :return: False if not a valid position
        """
        try:
            self.grid[coords[1]][coords[0]] = objeto
        except IndexError:
            return False


class Handler(Mapa):
    def __init__(self, alto, ancho, colors, percentage=25, clean=True, headlimit=1, max_length=-1,
                 random_weight=True, crazy_behaviour=False, max_jump=2, body_char = "#", head_char = "O"):
        """
        Constructor class for Handler
        :param alto: Height
        :param ancho: Width
        :param colors: List of available colors
        :param percentage: Probability of creating a new snake
        :param clean: Shall I clean the corpses?
        :param headlimit: Maximum snakes, infinite if negative
        :param max_length: Max length of snakes, infinite if negative
        :param random_weight: Shall I random-weight the snakes?
        :param crazy_behaviour: Shall I create random-behavioured snakes?
        :param max_jump: If crazy_behaviour, Which should be the maximum variation for both axes?
        """
        super().__init__(alto, ancho)
        self.percentage = percentage
        self.clear = clean
        self.limit_length = max_length
        self.random_weight = random_weight
        self.crazy_behaviour = crazy_behaviour
        self.max_jump = max_jump
        self.colors = colors
        self.grid = self.gen_grid()
        self.heads = []
        self.removing = []
        self.head_limit = headlimit
        self.max_length = 0
        self.body_char = body_char
        self.head_char = head_char

    def run(self, gen=True):
        """
        Runs a turn
        :param gen: Shall I generate new snakes?
        :return: Status dictionary
        """
        delete = []
        if gen:
            self.gen_head()  # Gen the heads
        for x in range(0, len(self.heads)):  # Updates the heads
            die = self.heads[x].run(self)
            if die:
                if not self.heads[x].trigered:
                    self.removing.append(self.heads[x].start_coordinates)
                    # We set that there's a new snake that needs a meatgrinder session
                delete.append(self.heads[x])
        for x in delete:
            self.heads.remove(x)
        if self.clear:
            self.clean()  # Do some magic, just don't touch it
        return self.status()

    def status(self):
        """
        Generates the status dictionary
        :return: {"snakes", "average length", "removing", "max_length"}
        """
        heads = self.heads
        sum_length = 0
        for x in heads:
            sum_length += x.length
            if x.length > self.max_length:
                self.max_length = x.length
        try:
            average = sum_length / len(heads)
        except ZeroDivisionError:
            average = 0
        returneo = {"snakes": len(self.heads), "average length": average, "removing": len(self.removing),
                    "max_length": self.max_length}
        return returneo

    def clean(self):  # Harry Potter would be proud of this method
        """
        Cleans the game from corpses
        :return: VOID
        """
        remove = []  # We store the coords of the snakes that has been deleted completly
        for x in range(0, len(self.removing)):
            coords = self.removing[x]
            tile = self.get_coords(coords)
            nexts = tile.nextone  # We store the next position of the snake
            self.removing[x] = nexts
            if nexts == coords:  # This means that it was the last position so we delete it from erasing list
                remove.append(coords)
            self.set_coords(coords, Tile(coords))  # Finally, we clean the tile
        for x in remove:
            self.removing.remove(x)  # And now, he would hit me 'cause a magician never show its tricks

    def gen_head(self):
        """
        Generates a new head
        :return: VOID
        """
        percentage = self.percentage
        while percentage > 0:
            percentage -= 100
            if random.randint(0, 100) <= self.percentage and len(self.heads) != self.head_limit:
                salir = False
                while not salir:
                    coords = (random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1))
                    if self.get_coords(coords).transitable:
                        ia = IA(random_weight=self.random_weight, crazy_behaviour=self.crazy_behaviour,
                                max_jump=self.max_jump)
                        head = Head(coords, character=self.head_char, color=self.random_color(), transitable=False,
                                    behaviour=ia, limit=self.limit_length, body_char=self.body_char)
                        self.heads.append(head)
                        self.set_coords(coords, head)
                        salir = True
            else:
                percentage = -1

    def random_color(self):
        """
        Returns a random color index
        :return: Random color index
        """
        return random.choice(self.colors)


def options():
    ayuda = "List of allowed parameters:\n-c True/False : Clear corpses?\n-p Int: Probability of creating a new snake" \
            "\n-f Int: Number of fps\n-m Int: Max length of snakes\n-l Int: Limit of snakes\n-r True/False: " \
            "Random weighted choices?\n-z True/False: Crazy behaviour?\n-j True/False: Just calculating?\n" \
            "-o Int: Number of loop to calculate if just calculating\n-e Int: Random seed to be used(String " \
            "if random seed)\n-d Boolean: Shall I reset if the map is filled?" \
            "\n-t Int: If d, How much time shall I wait?\n-h Char: Character to represent the head of the snakes\n" \
            "-b Char: Character to represent the body of the snakes"
    import sys
    import getopt
    true = ["TRUE", "True", "true", "1"]
    returneo = {"clear": True, "percentage": 100, "fps": 10, "max_length": 30, "limit": -1, "random_weighted": True,
                "crazy": False, "justCalculating": False, "cicles": 6000, "seed": False, "filled": True,
                "timeout": 10, "head": "O", "body": "#"}
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "c:p:f:l:m:r:z:j:o:e:r:d:t:b:h:", ["help"])
    except Exception as e:
        print(str(e) + "\n" + ayuda)
        sys.exit()
    opciones = {"c": "clear", "p": "percentage", "f": "fps", "m": "max_length", "l": "limit", "r": "random_weighted",
                "z": "crazy", "j": "justCalculating", "o": "cicles", "e": "seed", "d": "filled", "t": "timeout",
                "h": "head", "b": "body"}
    for x in opts:
        flag = x[0].replace("-", "")
        if flag == "help":
            print(ayuda)
            sys.exit()
        option = opciones[flag]
        if option in ("clear", "random_weighted", "crazy", "justCalculating", "filled"):
            returneo[option] = x[1] in true
        elif option in ("percentage", "fps", "max_length", "limit", "cicles", "timeout"):
            try:
                returneo[option] = int(x[1])
            except ValueError:
                print("Flag \"" + flag + "\" couldn't be converted to integer. Exiting...")
                sys.exit()
        elif option in ("head", "body"):
            if len(x[1]) != 1:
                print("Invalid character")
                print(ayuda)
                sys.exit()
            else:
                returneo[option] = x[1]
        elif option == "seed":
            try:
                returneo[option] = int(x[1])
            except:
                returneo[option] = False
        else:
            print("Option {0} unhandled. Exiting...".format(option))
            sys.exit()
    return returneo


def main(stdscr, config):  # The root method, do not annoy him
    curses.curs_set(0)
    size = shutil.get_terminal_size()  # Gets terminal size so curses won't complain
    curses.start_color()
    curses.use_default_colors()
    colors = []
    for i in range(0, curses.COLORS):  # Curses shit
        curses.init_pair(i + 1, i, -1)
        colors.append(i)
    mapa = Handler(size[1] - 1, size[0] - 1, colors, clean=config["clear"] is True,
                   percentage=int(config["percentage"]),
                   max_length=int(config["max_length"]), headlimit=int(config["limit"]),
                   random_weight=config["random_weighted"] is True, crazy_behaviour=config["crazy"] is True,
                   body_char=config["body"], head_char=config["head"])
    # We init the game class, just read
    if config["seed"] is not False:  # We try to set the seed of the random module based on the config
        random.seed(a=int(config["seed"]))
    else:
        random.seed(a=random.randint(0, 100))
    if config["justCalculating"] is not True:  # Graphic Mode
        import time
        while True:
            tmpsize = shutil.get_terminal_size()
            tiempo = time.time()
            if config["filled"]:
                def alarma(signum, frame):
                    raise curses.error
                signal.signal(signal.SIGALRM, alarma)
                signal.alarm(config["timeout"])
            mapa.run(gen=True)
            try:
                mapa.print_grid(stdscr)
            except KeyboardInterrupt:
                exit()
            if tmpsize != size:  # If the window has been resized, relaunch the app
                size = tmpsize
                raise curses.error
            tiempo = time.time() - tiempo
            try:
                time.sleep(1 / int(config["fps"]) - tiempo)
            except KeyboardInterrupt:
                exit()
            except:
                pass
    else:  # Verbose Mode
        returneo = None
        for x in range(0, int(config["cicles"])):
            returneo = mapa.run(gen=True)
        stdscr.addstr(str(returneo))
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    while True:
        config = options()
        try:
            curses.wrapper(main, config)
        except KeyboardInterrupt:
            exit()
        except curses.error:
            pass
