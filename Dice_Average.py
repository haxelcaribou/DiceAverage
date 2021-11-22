#!/usr/bin/python3

import re
import math
from os import system, name
import operator

# At this point I'm just making a math interpeter

# import the readline module for arrow functionality if it exists
try:
    import readline
    readline.set_history_length(100)
except ImportError:
    pass


STATS_GRAPH = False


class ANSI:
    '''define ANSI colors'''
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BLACK = '\033[30m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    CLEAR = '\033[2J\033[H'


class Dist:
    def __init__(self, arg1=None):
        if arg1 is None:
            self.dist = {}
        elif isinstance(arg1, Dist):
            self.dist = arg1.dist
        elif isinstance(arg1, dict):
            self.dist = arg1
        elif isinstance(arg1, (int, float)):
            self.dist = {arg1: 1}
        else:
            raise ValueError()

    def __str__(self):
        return str(self.dist)

    def __len__(self):
        return len(self.dist)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for val in self.dist:
            if not val in other.dist:
                return False
            if self.dist[val] != other.dist[val]:
                return False
        return True

    def cartesian(self, other, op):
        new_stats = {}

        for n1 in self.dist:
            for n2 in other.dist:
                if op(n1, n2) in new_stats:
                    new_stats[op(n1, n2)] += self.dist[n1] + other.dist[n2] - 1
                else:
                    new_stats[op(n1, n2)] = self.dist[n1] + other.dist[n2] - 1

        return Dist(new_stats)

    def __add__(self, other):
        if self.dist == {}:
            return other
        if other.dist == {}:
            return self

        return self.cartesian(other, operator.add)

    def __sub__(self, other):
        if self.dist == {}:
            return other
        if other.dist == {}:
            return self

        return self.cartesian(other, operator.sub)

    def __mul__(self, other):
        return self.cartesian(other, operator.mul)

    def __truediv__(self, other):
        return self.cartesian(other, operator.truediv)

    def __floordiv__(self, other):
        return self.cartesian(other, operator.floordiv)

    def __mod__(self, other):
        return self.cartesian(other, operator.mod)

    def __pow__(self, other):
        return self.cartesian(other, operator.pow)

    def __neg__(self):
        new_stats = {}
        for val in self.dist:
            new_stats[-val] = self.dist[val]
        return Dist(new_stats)

    def __abs__(self):
        new_stats = {}
        for val in self.dist:
            new_stats[abs(val)] = self.dist[val]
        return Dist(new_stats)


# set default answer
ans = 0

# compile regexes
DICE_REGEX = re.compile(r"^(\d+d\d+(?=( |$)))+")
DICE_NUMBER_REGEX = re.compile(r"^\d+(?=d)")
DICE_SIDES_REGEX = re.compile(r"(?<=d)\d+")
INT_REGEX = re.compile(r"^-? ?\d+$")
FLOAT_REGEX = re.compile(r"^-? ?\d*\.\d+$")
ADD_REGEX = re.compile(r"(\+|(?<=\w) ?-)")
MULT_REGEX = re.compile(r"([\*/%])")


def parse_string(input_string):
    '''take input string and decide where to send it'''
    input_string = input_string.strip()

    # if it's valid dice notation roll it
    if DICE_REGEX.match(input_string):
        return avg_dice(input_string)

    # convert numbers to integers
    if INT_REGEX.match(input_string):
        return Dist(int(input_string.replace(" ", "")))
    # also convert decimals
    if FLOAT_REGEX.match(input_string):
        return Dist(float(input_string.replace(" ", "")))

    # do math if there are any math symbols
    math_strings = ("+", "-", "*", "/", "%", "^")
    for sub in math_strings:
        if sub in input_string:
            return parse_math(input_string)

    raise ValueError("Invalid Input")


def avg_die(input_string):
    '''get the statstics for a single type of die'''
    # print(ANSI.GREEN + input_string + ANSI.END)

    num_dice = int(DICE_NUMBER_REGEX.search(input_string).group())
    dice_sides = int(DICE_SIDES_REGEX.search(input_string).group())
    if num_dice == 0 or dice_sides == 0:
        return Dist()

    stats = Dist()
    num_combinations = math.pow(dice_sides, num_dice)
    for i in range(num_dice):
        new_stats = {}
        for n in range(1, dice_sides + 1):
            new_stats[n] = 1
        stats = Dist(stats) + Dist(new_stats)

    #print(ANSI.BOLD, str(stats), ANSI.END, "\n", sep="")

    return stats


def avg_dice(input_string):
    '''get the statstics for multiple types of dice'''
    dice = input_string.split(" ")

    total = Dist()

    for die in dice:
        total = total + avg_die(die.strip())

    return total


def parse_math(input_string):
    '''Handle basic math'''
    if ADD_REGEX.search(input_string):
        parts = ADD_REGEX.split(input_string)
        sum = parse_string(parts[0])
        # output_string = "{:g}".format(sum)
        i = 1
        while i < len(parts):
            term = parse_string(parts[i + 1])
            if parts[i] == "+":
                sum = sum + term
                # output_string += " + "
            else:
                sum = sum - term
                # output_string += " - "
            # output_string += "{:g}".format(term)
            i += 2
        # print("{} = {:g}\n".format(output_string, sum))
        return sum

    if "*" in input_string or "/" in input_string or "%" in input_string:
        parts = MULT_REGEX.split(input_string)
        product = parse_string(parts[0])
        # output_string = "{:g}".format(product)
        i = 1
        while i < len(parts):
            term = parse_string(parts[i + 1])
            if parts[i] == "*":
                product = product * term
                # output_string += " * "
            elif parts[i] == "/":
                product = product / term
                # output_string += " / "
            else:
                product = product % term
                # output_string += " % "
            # output_string += "{:g}".format(term)
            i += 2
        # print("{} = {:g}\n".format(output_string, product))
        return product

    if "^" in input_string:
        parts = input_string.split("^", 1)
        base = parse_string(parts[0])
        exponent = parse_string(parts[1])
        power = base ** exponent
        # print("{:g} ^ {:g} = {:g}\n".format(base, exponent, power))
        return power

    if "-" in input_string:
        return -parse_string(input_string[1:])

    raise ValueError("Invalid Input")


def print_stats(stats):
    stats = stats.dist

    '''take the generated statistics and print them'''
    if stats == {}:
        return 0
    sum = 0
    amt = 0
    for val in stats:
        sum += val * stats[val]
        amt += stats[val]

    avg = sum / amt

    keys = stats.keys()

    print(ANSI.BOLD, "Average = {:g}".format(avg), ANSI.END, sep="")
    print(ANSI.BOLD, "Minimum = {:g}".format(min(keys)), ANSI.END, sep="")
    print(ANSI.BOLD, "Maximum = {:g}".format(max(keys)), ANSI.END, sep="")

    print()

    if STATS_GRAPH:
        for n in range(min(keys), max(keys) + 1):
            print("{:g}: ".format(n), end="", flush=True)
            if n in stats:
                for i in range(stats[n]):
                    print("@", end="", flush=True)
            print()

    return avg


def clear_screen():
    '''clear the terminal screen'''
    if name == 'nt':
        system('cls')
    elif name == "posix":
        system('clear')
    else:
        print(ANSI.CLEAR, end="")


def run():
    '''main program'''
    # clear screen at program start
    clear_screen()

    # keep taking commands
    while 1:
        # take input
        i = input(ANSI.BLUE + "Enter Value: " + ANSI.END).strip().lower()

        # quit program
        if i in ("exit", "end", "quit", "q"):
            clear_screen()
            break

        elif i == "clear":
            clear_screen()

        elif i == "":
            print("No Input Entered")

        else:
            try:
                ans = print_stats(parse_string(i))
            except ValueError as e:
                print(e)
            except ZeroDivisionError:
                print("Divide by Zero")


if __name__ == '__main__':
    run()
