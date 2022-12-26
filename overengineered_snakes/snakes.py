#! /usr/bin/env python

import shutil
import random
import curses
from backend import Handler
from overengineered_snakes.renderers.curses import CursesRenderer




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
    size = shutil.get_terminal_size()  # Gets terminal size so curses won't complain
    colors = []
    for i in range(0, curses.COLORS):  # Curses shit
        colors.append(i)
    mapa = Handler(size[1], size[0]-1, colors, clean=config["clear"] is True,
                   percentage=int(config["percentage"]),
                   max_length=int(config["max_length"]), headlimit=int(config["limit"]),
                   random_weight=config["random_weighted"] is True, crazy_behaviour=config["crazy"] is True,
                   body_char=config["body"], head_char=config["head"])
    renderer = CursesRenderer()
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
            status = mapa.run(gen=True)
            try:
                renderer.render(mapa)
            except KeyboardInterrupt:
                exit()
            if config["filled"] and status["filled"] and status["snakes"] == 0:
                time.sleep(config["timeout"])
                raise curses.error
            if tmpsize != size:  # If the window has been resized, relaunch the app
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
