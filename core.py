"""Core functions of Gregorian date manipulation.
See https://s2.org/~chery/date.html
The day 0 of the internal day counter is 0000-03-01 in the proleptic
Gregorian calendar.

In Python the //, %, and divmod operators round towards negative infinity.
Translations of these equations to other languages should take this into
account."""

week_epoch = -58

def divmoddiv(a, b, c):
    i, j = divmod(a, b)
    return i, j // c

def from_y_dy(y, dy):
    """(Year, day-in-year (zero = March 1st)) to internal day counter."""
    return 365*y + y//4 - y//100 + y//400 + dy

def from_gregorian(yg, mg, dg):
    """(Year, month, day) of Gregorian date to internal day counter."""
    y, my = divmod(12*yg + mg - 3, 12)
    return from_y_dy(y, (153*my + 2)//5 + dg - 1)

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
    """Internal day counter of easter in year."""
    c = y//100 + 1
    g = y % 19
    e = (15 - 11*g + 3*c//4 - (5 + 8*c)//25) % 30
    return 4 + (from_y_dy(y, 20 + e - (e + g//11) // 29) + 3) // 7 * 7

def weekday(d):
    """Internal day counter to range from Monday = 0 to Sunday = 6."""
    return (d + 2) % 7

def ceiling_weekday(d, wd):
    """First day which is weekday wd and not less than day d."""
    return (d + 8 - wd) // 7 * 7 - 2 + wd

def next_weekday(d, wd):
    """First day which is weekday wd and greater than day d."""
    return (d + 9 - wd) // 7 * 7 - 2 + wd

def previous_weekday(d, wd):
    """Last day which is weekday wd and less than day d."""
    return (d + 1 - wd) // 7 * 7 - 2 + wd

def floor_weekday(d, wd):
    """Last day which is weekday wd and not greater than day d."""
    return (d + 2 - wd) // 7 * 7 - 2 + wd
