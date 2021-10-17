#! /usr/bin/env python3

import sys
from os.path import dirname

sys.path.append(dirname(dirname(sys.path[0])))

import core
import step
from itertools import count
from operator import add
from functools import reduce

def holiday(g):
    easter = core.easter(g.year)
    md = g.month, g.day_of_month
    if md == (1, 1):
        return 'uusivuosi'
    if md == (1, 6):
        return 'loppiainen'
    if md == (5, 1):
        return 'vappu'
    if md == (12, 6):
        return 'itsenäisyyspäivä'
    if md == (12, 24):
        return 'jouluaatto'
    if md == (12, 25):
        return 'joulupäivä'
    if md == (12, 26):
        return 'tapaninpäivä'
    ediff = g.day - easter
    if ediff == -2:
        return 'pitkäperjantai'
    if ediff == 1:
        return 'toinen pääsiäispäivä'
    if ediff == 39:
        return 'helatorstai'
    if g.weekday == 4 and md >= (6, 19) and md <= (6, 25):
        return 'juhannusaatto'
    return None

def main():
    print('title,start,end,country')
    for g in step.generate_gregorian(core.from_gregorian(2019, 1, 1)):
        if g.year >= 2119:
            break
        hd = holiday(g)
        if hd:
            date = '%04d-%02d-%02d' % (g.year, g.month, g.day_of_month)
            print('%s,%s,%s,FI' % (hd, date, date))

if __name__ == '__main__':
    main()
