#!/usr/bin/python3

import random
import re
import math
from os import system, name

# At this point I'm just making a math interpeter

# import the readline module for arrow functionality if it exists
try:
    import readline
    readline.set_history_length(100)
except ImportError:
    pass


# define ANSI colors
class ANSI:
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


# set default answer
ans = 0

# compile regexes
diceRegex = re.compile(r"^(\d+d\d+(?=( |$)))+")
diceNumberRegex = re.compile(r"^\d+(?=d)")
diceSidesRegex = re.compile(r"(?<=d)\d+")


def parseString(input):
    input = input.strip()

    # if it's valid dice notation roll it
    if diceRegex.match(input):
        return avgDice(input)

    raise ValueError("Invalid Input")


def avgDie(input):
    print(ANSI.GREEN + input + ANSI.END)

    numDice = int(diceNumberRegex.search(input).group())
    diceSides = int(diceSidesRegex.search(input).group())
    if numDice == 0 or diceSides == 0:
        return {}

    stats = {}
    numCombinations = math.pow(diceSides, numDice)
    for i in range(numDice):
        newStats = {}
        for n in range(1, diceSides+1):
            newStats[n] = 1;
        stats = addStats(stats, newStats)

    #print(ANSI.BOLD, str(stats), ANSI.END, "\n", sep="")

    return stats


def avgDice(input):
    dice = input.split(" ")

    total = {}

    for die in dice:
        total = addStats(total,avgDie(die.strip()))

    return total


def addStats(stats1, stats2):
    if stats1 == {}:
        return stats2
    if stats2 == {}:
        return stats1

    newStats = {}

    for n1 in stats1:
        for n2 in stats2:
            newStats[n1+n2] = stats1[n1] + stats2[n2]

    return newStats


def getStats(stats):
    if stats == {}:
        return 0
    sum = 0
    amt = 0
    for val in stats:
        sum += val*stats[val]
        amt += stats[val]

    avg = sum/amt

    keys = stats.keys()

    print(ANSI.BOLD, "Average = {:g}".format(avg), ANSI.END, sep="")
    print(ANSI.BOLD, "Minimum = {:g}".format(min(keys)), ANSI.END, sep="")
    print(ANSI.BOLD, "Maximum = {:g}".format(max(keys)), ANSI.END, sep="")

    return avg


def clearScreen():
    if name == 'nt':
        system('cls')
    elif name == "posix":
        system('clear')
    else:
        print(ANSI.CLEAR, end="")


def run():
    # clear screen at program start
    clearScreen()

    # keep taking commands
    while 1:
        # take input
        i = input(ANSI.BLUE + "Enter Value: " + ANSI.END).strip().lower()

        # help
        if i == "help" or i == "info":
            print()
            print(helpText)

        # quit program
        elif i == "exit" or i == "end" or i == "quit" or i == "q":
            clearScreen()
            break

        elif i == "clear":
            clearScreen()

        elif i == "":
            print("No Input Entered")

        else:
            try:
                ans = getStats(parseString(i))
            except ValueError as e:
                print(e)
            except ZeroDivisionError:
                print("Divide by Zero")


if __name__ == '__main__':
    run()
