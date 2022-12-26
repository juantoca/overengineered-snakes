from __future__ import annotations

from overengineered_snakes.configs.config import Config


def options():
    ayuda = (
        "List of allowed parameters:\n"
        "-c True/False : Clear corpses?\n"
        "-p Int: Probability of creating a new snake\n"
        "-f Int: Number of fps\n-m Int: Max length of snakes\n"
        "-l Int: Limit of snakes\n"
        "-r True/False: Random weighted choices?\n"
        "-z True/False: Crazy behaviour?\n-j True/False: Just calculating?\n"
        "-o Int: Number of loop to calculate if just calculating\n"
        "-e Int: Random seed to be used(String if random seed)\n"
        "-d Boolean: Shall I reset if the map is filled?\n"
        "-t Int: If d, How much time shall I wait?\n"
        "-h Char: Character to represent the head of the snakes\n"
        "-b Char: Character to represent the body of the snakes"
    )
    import sys
    import getopt

    true = ["TRUE", "True", "true", "1"]
    returneo = {
        "clear": True,
        "percentage": 100,
        "fps": 10,
        "max_length": 30,
        "limit": -1,
        "random_weighted": True,
        "crazy": False,
        "justCalculating": False,
        "cicles": 6000,
        "seed": False,
        "filled": True,
        "timeout": 10,
        "head": "O",
        "body": "#",
    }
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(
            argv,
            "c:p:f:l:m:r:z:j:o:e:r:d:t:b:h:",
            ["help"],
        )
    except Exception as e:
        print(str(e) + "\n" + ayuda)
        sys.exit()
    opciones = {
        "c": "clear",
        "p": "percentage",
        "f": "fps",
        "m": "max_length",
        "l": "limit",
        "r": "random_weighted",
        "z": "crazy",
        "j": "justCalculating",
        "o": "cicles",
        "e": "seed",
        "d": "filled",
        "t": "timeout",
        "h": "head",
        "b": "body",
    }
    for x in opts:
        flag = x[0].replace("-", "")
        if flag == "help":
            print(ayuda)
            sys.exit()
        option = opciones[flag]
        if option in ("clear", "random_weighted", "crazy", "justCalculating", "filled"):
            returneo[option] = x[1] in true
        elif option in (
            "percentage",
            "fps",
            "max_length",
            "limit",
            "cicles",
            "timeout",
        ):
            try:
                returneo[option] = int(x[1])
            except ValueError:
                print(
                    'Flag "' + flag + "\" couldn't be converted to integer. Exiting...",
                )
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
            except:  # noqa: E722
                returneo[option] = False
        else:
            print(f"Option {option} unhandled. Exiting...")
            sys.exit()
    return Config(**returneo)
