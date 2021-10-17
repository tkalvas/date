#! /usr/bin/env python3

import sys
from os.path import dirname

sys.path.append(dirname(dirname(sys.path[0])))

import core
import step
from itertools import count
from operator import add
from functools import reduce

def year_type(year):
    leap = year % 400 == 0 or year % 4 == 0 and year % 100 != 0
    easter = core.easter(year) - core.from_gregorian(year, 3, 22)
    return 2 * easter + +leap

def workday(g, easter):
    md = g.month, g.day_of_month
    if g.weekday >= 5:
        return False
    if md in [(1, 1), (1, 6), (5, 1), (12, 6), (12, 24), (12, 25), (12, 26)]:
        return False
    if g.day - easter in [-2, 1, 39]:
        return False
    if g.weekday == 4 and md >= (6, 19) and md <= (6, 25):
        return False
    return True

def year_months(year):
    months = 12 * [0]
    easter = core.easter(year)
    for g in step.generate_gregorian(core.from_gregorian(year, 1, 1)):
        if g.year != year:
            break
        if workday(g, easter):
            months[g.month - 1] += 1
    return months

def lookup(years):
    r = ''
    for i in range(0, 70):
        for m in range(0, 12):
            r += chr(48 + years[i][m] - 17)
    return r

def lookup2(years):
    r = ''
    for i in range(0, 70, 2):
        for m in range(0, 12):
            l = years[i][m] - 17
            h = years[i+1][m] - 17
            r += chr(42 + 7*h + l)
    return r

settings = {
    "comma": ",",
    "year": "year(B2)",
    "month": "month(B2)",
    "day": "B2"
}

def x_call(name):
    return lambda *args: name + '(' + x_comma().join(map(str, args)) + ')'

def x_comma():
    return settings["comma"]

def x_year():
    return settings["year"]

def x_month():
    return settings["month"]

def x_day():
    return settings["day"]

x_day_of_month = x_call('day')
x_div = x_call('quotient')
x_mod = x_call('mod')
x_choose = x_call('choose')
x_date = x_call('date')
x_weekday = x_call('weekday')
x_code = x_call('code')
x_mid = x_call('mid')
x_iferror = x_call('iferror')
x_if = x_call('if')
x_and = x_call('and')
x_match = x_call('match')

def x_set(*args):
    return '{' + x_comma().join(map(str, args)) + '}'

def x_parens(arg):
    return '(' + arg + ')'

def x_c():
    return x_parens(x_div(x_year(), 100) + '+1')

def x_g():
    return x_mod(x_year(), 19)

def x_e():
    return x_mod('255-11*' + x_g() + '+' + x_div('3*' + x_c(), 4) +\
                 '-' + x_div('5+8*' + x_c(), 25), 30)

def x_pfm():
    return x_e() + '-' + x_div(x_e() + '+' + x_div(x_g(), 11), 29)

def x_eweekday():
    return 'mod(2+' + x_year() + '+quotient(' + x_year() + x_comma() +\
        '4)-quotient(' + x_year() + x_comma() + '100)+quotient(' +\
        x_year() + x_comma() + '400)' + x_comma() + '7)'

def x_easter():
    """Led to longer formula than easter2 because of duplication of pfm."""
    return '(' + x_pfm() + '+6-mod(' + x_pfm() + '+' + x_eweekday() +\
        x_comma() + '7))'

def x_easter2():
    """n = y + y//4 - y//100 + y//400; (n+23+pfm)//7*7-(n+17)"""
    return x_parens(x_div(x_year() + '+' + x_div(x_year(), 4) + '-'
                          + x_div(x_year(), 100) + '+' + x_div(x_year(), 400)
                          + '+23+' + x_pfm(),
                          7)
                    + '*7-' + x_year() + '-' + x_div(x_year(), 4) + '+'
                    + x_div(x_year(), 100) + '-' + x_div(x_year(), 400) + '-17')

def x_leap():
    return x_parens(x_parens(x_date(x_year(), 3, 1) + '-'
                             + x_date(x_year(), 2, 29))
                    + '-1')

def x_leap2():
    """7 if leap year, 1 if not"""
    return '6*' + x_parens(x_date(x_year(), 3, 1) + '-'
                           + x_date(x_year(), 2, 28)) + '-5'

def x_index():
    return '24*' + x_easter2() + '+12*' + x_leap() + '+' + x_month()

def formula(years):
    return "=17+mid(\"" + lookup(years) + "\"" + x_comma() + x_index() +\
        x_comma() + "1)"

def formula2(years):
    return "=17+mod(" + x_div("code(mid(\"" + lookup2(years) + "\"" + x_comma() +
                          '12*' + x_easter2() + '+' + x_month() + x_comma() +
                          "1))-42",
                          x_leap2()) + x_comma() + "7)"

def easter_diff():
    return x_day() + '-' + x_parens(x_date(x_year(), 3, 22) + '+' + x_easter2())

def weekend():
    return x_choose(x_weekday(x_day(), 3) + '+1', *[0, 0, 0, 0, 0, 1, 1])

def fixed_holiday():
    return x_iferror(x_match('31*' + x_mod('12*' + x_year() + '+' + x_month()
                                           + '-3',
                                           12)
                             + '+' + x_day_of_month(x_day()),
                             x_set(63, 285, 303, 304, 305, 311, 316),
                             0),
                     0)

def easter_holiday():
    return x_iferror(x_match(easter_diff(), x_set(-2, 1, 39), 0), 0)

def midsummer_eve():
    return x_if(x_and(x_div(x_day() + '-' + x_date(x_year(), 6, 19) + '+364', 7)
                      + '=52',
                      x_weekday(x_day(), 3) + '=4'),
                1, 0)

def day_formula():
    return '=' + weekend() + '+' + fixed_holiday() + '+' + easter_holiday() +\
        '+' + midsummer_eve()

def main():
    years = {}
    for year in count(2000):
        i = year_type(year)
        if i not in years:
            years[i] = year
        if len(years) == 70:
            break
    #print(years)
    ys = []
    tots = []
    for i in range(0, 70):
        ys.append(year_months(years[i]))
        tots.append(reduce(add, ys[-1]))
    #print(formula(ys))
    print(formula2(ys))
    #print('=' + x_easter())
    #print('=' + x_easter2())
    #print('=' + x_index())
    #print(tots)
    #print(lookup2(ys))
    #print([lookup(ys)[24*i+12+2-1] for i in range(0, 35)])
    #print(lookup(ys)[601])
    #print()
    #print(year_type(2019), year_months(2019))
    print()
    print(day_formula())

if __name__ == '__main__':
    main()

