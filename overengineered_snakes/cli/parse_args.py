from __future__ import annotations

import argparse

from overengineered_snakes.configs.config import Config


def get_config() -> Config:
    parser = argparse.ArgumentParser(
        prog="snakes",
        description="A ZPG simulation of several snakes",
    )
    parser.add_argument(
        "-c",
        "--dont-clear",
        action="store_true",
        help="Controls if dead snakes should be cleaned up",
    )
    parser.add_argument(
        "-p",
        "--probability",
        default=100,
        type=int,
        help="Probability of creating a new snake in each frame",
    )
    parser.add_argument(
        "-f",
        "--fps",
        default=10,
        type=int,
        help="Number of frames per second",
    )
    parser.add_argument(
        "-l",
        "--length",
        default=-1,
        type=int,
        help="Length limit of the snakes",
    )
    parser.add_argument(
        "-n",
        "--num_snakes",
        default=-1,
        type=int,
        help="Maximum number of snakes",
    )
    parser.add_argument(
        "-r",
        "--random-weights",
        action="store_true",
        help="Controls if the weights of the snakes decisions should be randomized",
    )
    parser.add_argument(
        "-z",
        "--crazy",
        action="store_true",
        help="Controls if the snake possible movements are randomized",
    )
    parser.add_argument(
        "-j",
        "--headless",
        help="Controls if the program should run in headless mode",
    )
    parser.add_argument(
        "-o",
        "--cycles",
        default=6000,
        type=int,
        help="Cycles to compute when just computing",
    )
    parser.add_argument(
        "-e",
        "--seed",
        default=False,
        type=int,
        help="Random seed to use",
    )
    parser.add_argument(
        "-d",
        "--reset",
        action="store_true",
        help="Controls if the map should be reset when filled",
    )
    parser.add_argument(
        "-t",
        "--reset-time",
        default=10,
        type=int,
        help="Controls how much time should be waited before reseting the map",
    )
    parser.add_argument(
        "--head",
        default="O",
        type=str,
        help="Character that represents the head of the snakes",
    )
    parser.add_argument(
        "--body",
        default="#",
        type=str,
        help="Character that represents the body of the snakes",
    )
    args: argparse.Namespace = parser.parse_args()
    return Config(
        clear=not args.dont_clear,
        percentage=args.probability,
        fps=args.fps,
        max_length=args.length,
        limit=args.num_snakes,
        random_weighted=args.random_weights,
        crazy=args.crazy,
        justCalculating=args.headless,
        cicles=args.cycles,
        seed=args.seed,
        filled=args.reset,
        timeout=args.reset_time,
        head=args.head,
        body=args.body,
    )
