"""Epoch values and conversions.
The day 0 of the internal day counter is 0000-02-01 in the proleptic
Gregorian calendar. Julian date 0 is noon, January 1, 4713 BC in
the Julian calendar. Reduced Julian date is Julian date - 2 400 000.
Lilian date 1 is October 15, 1582, the actual beginning of the
Gregorian calendar. Rata Die 1 is January 1, 1 in the proleptic
Gregorian calendar."""

from core import divmoddiv

julian_epoch = -1721119.5

def to_julian_date(d):
    """Internal day counter to Julian date (number)."""
    return d - julian_epoch

def from_julian_date(jd):
    """Julian date (number) to internal day counter."""
    return jd + julian_epoch

reduced_julian_epoch = 678880.5

def to_reduced_julian_date(d):
    """Internal day counter to Reduced Julian date."""
    return d - reduced_julian_epoch

def from_reduced_julian_date(rjd):
    """Reduced Julian date to internal day counter."""
    return rjd + reduced_julian_epoch

lilian_epoch = 578040

def to_lilian_date(d):
    """Internal day counter to Lilian date."""
    return d - lilian_epoch

def from_lilian_date(ld):
    """Lilian date to internal day counter."""
    return ld + lilian_epoch

rata_die_epoch = 305

def to_rata_die(d):
    """Internal day counter to Rata Die."""
    return d - rata_die_epoch

def from_rata_die(rd):
    """Rata Die to internal day counter."""
    return rd + rata_die_epoch

