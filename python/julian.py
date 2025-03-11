"""Julian calendar handling."""

from core import divmoddiv

def to_no_zero(i):
    """Transform [..., -1, 0, 1, ...] to [..., -2, -1, 1, ...]"""
    return i if i > 0 else i - 1

def from_no_zero(i):
    """Transform [..., -2, -1, 1, ...] to [..., -1, 0, 1, ...]"""
    return i if i > 0 else i + 1

# Saturday, January 1, 1 AD (Julian) was 2 days before
# Monday, January 1, 1 AD (Gregorian)
julian_gregorian_base_offset = 2

def to_julian(d):
    """Internal day counter to (year, month, day) of Julian date."""
    d2 = d + julian_gregorian_base_offset
    y, dy = divmoddiv(d2 * 4 + 3, 1461, 4)
    my, dm = divmoddiv(5*dy + 2, 153, 5)
    yj0, mj0 = divmod(12*y + my + 2, 12)
    return to_no_zero(yj0), mj0 + 1, dm + 1

def from_julian_y_dy(y, dy):
    """(Year, day-in-year (zero = March 1st)) to internal day counter."""
    return 365*y + y//4 + dy - julian_gregorian_base_offset

def from_julian(yj1, mj, dj):
    """(Year, month, day) of Julian date to internal day counter."""
    yj = from_no_zero(yj1)
    y, my = divmod(12*yj + mj - 3, 12)
    return from_julian_y_dy(y, (153*my + 2)//5 + dj - 1)
