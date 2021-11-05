#!/usr/bin/python3

import random
import re
import math
from os import system, name

# At this point I'm just making a math interpeter

# TODO
# option to get average, min, and max of rolls instead of specific roll value
# - How to deal with functions more complication than simple operators
# - Possible simpler and seperate method or even seperate program entirely


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
diceRegex = re.compile(r"^(\d+d\d+((t|b)\d+)?(?=( |$)))+")
addRegex = re.compile(r"(-|\+)")
intRegex = re.compile(r"^\d+$")


def parseString(input):
    input = input.strip()

    # convert numbers to integers
    if intRegex.match(input):
        return int(input.replace(" ", ""))

    # do math if there are any math symbols
    mathStrings = ("+", "-")
    for sub in mathStrings:
        if sub in input:
            return parseMath(input)

    # if it's valid dice notation roll it
    if diceRegex.match(input):
        return avgDice(input)

    # if either side of a math expression is empty replace it with zero
    if input == "":
        return 0

    # gives the last valid answer
    if input == "ans":
        return ans

    # handle shortcuts
    if input == "t":
        return avgDie("1d20")
    if input == "a":
        return avgDie("2d20b1")
    if input == "d":
        return avgDie("2d20t1")
    if input == "s":
        return avgDie("4d6b1")

    raise ValueError("Invalid Input")


def parseMath(input):
    parts = addRegex.split(input)
    sum = parseString(parts[0])
    output_string = "{:g}".format(sum)
    i = 1
    while i < len(parts):
        term = parseString(parts[i + 1])
        if parts[i] == "+":
            sum += term
            output_string += " + "
        elif parts[i] == "-":
            sum -= term
            output_string += " - "
        else:
            raise ValueError("Unknown operator")
        output_string += "{:g}".format(term)
        i += 2
    print("{} = {:g}\n".format(output_string, sum))
    return sum


def avgDie(input):
    print(ANSI.GREEN + input + ANSI.END)

    numDice = int(re.search(r"^\d+(?=d)", input).group())
    diceSides = int(re.search(r"(?<=d)\d+", input).group())
    if numDice == 0 or diceSides == 0:
        return 0

    tSearch = re.search(r"(?<=t)\d+$", input)
    bSearch = re.search(r"(?<=b)\d+$", input)
    if tSearch:
        return removeDice(numDice, diceSides, int(tSearch.group()), True)
    elif bSearch:
        return removeDice(numDice, diceSides, int(bSearch.group()), False)

    sum = (diceSides + 1)/2 * numDice

    print(ANSI.BOLD, str(sum), ANSI.END, "\n", sep="")

    return sum


def removeDice(num, dice, remove, top):
    raise ValueError("Not yet implemented")

    rolls = []

    # roll num number of times
    for i in range(num):
        # get random number in range dice
        roll = random.randint(1, dice)
        info = {"roll": roll,
                "order": i,
                "removed": False}
        rolls.append(info)

    sortedRolls = sorted(rolls, key=lambda item: item.get("roll"))

    if remove > num:
        raise ValueError("More dice removed than rolled")

    # print and sum
    if top:
        for i in range(remove):
            rolls[sortedRolls[len(rolls) - i - 1]["order"]]["removed"] = True
    else:
        for i in range(remove):
            rolls[sortedRolls[i]["order"]]["removed"] = True

    sum = 0

    # print and sum
    for roll in rolls:
        n = roll["roll"]
        if roll["removed"]:
            print(ANSI.RED, str(n), ANSI.END, sep="", end=" ", flush=True)
        else:
            print(n, end=" ", flush=True)
            sum += n

    print("\n", ANSI.BOLD, str(sum), ANSI.END, "\n", sep="")

    return sum


def avgDice(input):
    dice = input.split(" ")

    total = 0

    for die in dice:
        total += avgDie(die.strip())

    return total


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
                ans = parseString(i)
                print(ANSI.BOLD, "Average = {:g}".format(ans), ANSI.END, sep="")
            except ValueError as e:
                print(e)
            except ZeroDivisionError:
                print("Divide by Zero")

if __name__ == '__main__':
    run()
