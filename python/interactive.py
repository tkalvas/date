from core import *
from check import *
from types import SimpleNamespace
from itertools import count, islice
from collections import defaultdict

def days_from(d):
    return count(start=d)

def xdays_from(d):
    return map(extend_day, days_from(d))

def extend_day(d):
    yg, mg, dg = to_gregorian(d)
    yi, wi, di = to_iso_week_date(d)
    return SimpleNamespace(day=d,
                           year=yg,
                           month=mg,
                           day_of_month=dg,
                           week_year=yi,
                           week=wi,
                           day_of_week=di)

def xcount(it):
    counts = defaultdict(int)
    for elem in it:
        counts[elem] += 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)

def xdays_of_146097():
    return islice(xdays_from(from_gregorian(2001, 1, 1)), 0, 146097)

## Getting the distribution of weekdays for 13th of any month:
## > xcount([d.day_of_week for d in xdays_of_146097() if d.day_of_month == 13])
## [(5, 688), (7, 687), (3, 687), (2, 685), (1, 685), (6, 684), (4, 684)]
