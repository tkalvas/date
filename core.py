week_epoch = -58

def divmoddiv(a, b, c):
    i, j = divmod(a, b)
    return i, j // c

def from_gregorian(yg, mg, dg):
    """(Year, month, day) of Gregorian date to internal day counter."""
    y, my = divmod(12*yg + mg - 3, 12)
    dy = (153*my + 2)//5 + dg - 1
    return 365*y + y//4 - y//100 + y//400 + dy

def to_gregorian(d):
    """Internal day counter to (year, month, day) of Gregorian date."""
    y, dy = divmoddiv((d + (4*d + 146101)//146097*3//4) * 4 + 3, 1461, 4)
    my, dm = divmoddiv(5*dy + 2, 153, 5)
    yg, mg0 = divmod(12*y + my + 2, 12)
    return yg, mg0 + 1, dm + 1

def from_iso_week_date(yi, wi, di):
    """(Year, week, weekday) of ISO 8601 week-format date to internal
    day counter."""
    w = (1461*yi + 7 - 4*((yi - 1)//100 - yi//400)) // 28 + wi - 1
    return 7*w + di - 1 + week_epoch

def to_iso_week_date(d):
    """Internal day counter to (year, week, weekday) of ISO 8601 week-format
    date."""
    w, dw = divmod(d - week_epoch, 7)
    yi, wy = divmoddiv(28*w + 20 - 4*(5269 - w)//20871*3//4*4, 1461, 28)
    return yi, wy + 1, dw + 1

def easter(y):
    c = y//100 + 1
    g = y % 19
    e = (15 - 11*g + 3*c//4 - (5 + 8*c)//25) % 30
    d = e - (e + g//11) // 29
    p = 365*y + y//4 - y//100 + y//400 + 20 + d
    return p + 1 + (3 - p)%7

def weekday(d):
    """Internal day counter to range from Monday = 0 to Sunday = 6."""
    return (d + 2) % 7
