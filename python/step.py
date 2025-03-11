import core
import julian
from types import SimpleNamespace

def generate_gregorian(d):
    yg, mg, dg = core.to_gregorian(d)
    wd = core.weekday(d)
    while True:
        yield SimpleNamespace(day=d,
                              year=yg,
                              month=mg,
                              day_of_month=dg,
                              weekday=wd)
        if (mg, dg) == (2, 28):
            if yg % 400 == 0 or yg % 4 == 0 and yg % 100 != 0:
                dg = 29
            else:
                mg, dg = 3, 1
        else:
            dg += 1
            if dg > [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mg]:
                mg += 1
                dg = 1
                if mg > 12:
                    yg += 1
                    mg = 1
        d += 1
        wd = (wd + 1) % 7

def generate_iso_week_date(d):
    yi, wi, di = core.to_iso_week_date(d)
    gregorian_iter = generate_gregorian(d)
    next(gregorian_iter)
    while True:
        yield SimpleNamespace(day=d,
                              year=yi,
                              week=wi,
                              day_of_week=di)
        gregorian = next(gregorian_iter)
        yg, mg, dg = gregorian.year, gregorian.month, gregorian.day_of_month
        di += 1
        if di > 7:
            wi += 1
            di = 1
            if (mg, dg) >= (12, 29) or (mg, dg) <= (1, 4):
                yi += 1
                wi = 1
        d += 1

def generate_julian(d):
    yj, mj, dj = julian.to_julian(d)
    wd = core.weekday(d)
    while True:
        yield SimpleNamespace(day=d,
                              year=yj,
                              month=mj,
                              day_of_month=dj,
                              weekday=wd)
        if (mj, dj) == (2, 28):
            if yj % 4 == 0:
                dj = 29
            else:
                mj, dj = 3, 1
        else:
            dj += 1
            if dj > [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mj]:
                mj += 1
                dj = 1
                if mj > 12:
                    yj += 1
                    if yj == 0:
                        yj = 1
                    mj = 1
        d += 1
        wd = (wd + 1) % 7
