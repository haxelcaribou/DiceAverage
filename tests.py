#!/usr/bin/python3

import unittest
import math

import Dice_Average as dice
from Dice_Average import Dist


class TestDiceRoller(unittest.TestCase):
    def test_math(self):
        self.assertEqual(dice.parse_math("-1"), Dist(-1))
        self.assertEqual(dice.parse_math("-10"), Dist(-10))
        self.assertEqual(dice.parse_math("-1030"), Dist(-1030))

        self.assertEqual(dice.parse_math("1+1"), Dist(2))
        self.assertEqual(dice.parse_math("1+10"), Dist(11))
        self.assertEqual(dice.parse_math("10+20+30"), Dist(60))

        self.assertEqual(dice.parse_math("1-1"), Dist(0))
        self.assertEqual(dice.parse_math("1-10"), Dist(-9))
        self.assertEqual(dice.parse_math("10-20-30"), Dist(-40))

        self.assertEqual(dice.parse_math("1*1"), Dist(1))
        self.assertEqual(dice.parse_math("1*10"), Dist(10))
        self.assertEqual(dice.parse_math("10*20*30"), Dist(10 * 20 * 30))

        self.assertEqual(dice.parse_math("1/1"), Dist(1))
        self.assertEqual(dice.parse_math("1/10"), Dist(0.1))
        self.assertEqual(dice.parse_math("10/20/30"), Dist(10 / 20 / 30))

        self.assertEqual(dice.parse_math("2%2"), Dist(0))
        self.assertEqual(dice.parse_math("1%2"), Dist(1))
        self.assertEqual(dice.parse_math("11%10"), Dist(1))
        self.assertEqual(dice.parse_math("1030%30"), Dist(10))
        self.assertEqual(dice.parse_math("-2%2"), Dist(0))
        self.assertEqual(dice.parse_math("-1%2"), Dist(1))
        self.assertEqual(dice.parse_math("-11%10"), Dist(9))
        self.assertEqual(dice.parse_math("-1030%30"), Dist(20))

        self.assertEqual(dice.parse_math("1^1"), Dist(1))
        self.assertEqual(dice.parse_math("2^3"), Dist(8))
        self.assertEqual(dice.parse_math("10^0"), Dist(1))
        self.assertEqual(dice.parse_math("2^-2"), Dist(0.25))

        self.assertEqual(dice.parse_math("2*3-60*0.2"), Dist(-6))
        self.assertEqual(dice.parse_math("2^3-6/-6"), Dist(9))
        self.assertEqual(dice.parse_math("20%15/5+2"), Dist(3))

if __name__ == '__main__':
    # Main module
    unittest.main(buffer=True)
