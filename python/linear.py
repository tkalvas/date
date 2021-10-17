rata_die_epoch = 306
julian_date_epoch = -1721119.5
lilian_epoch = 578041
unix_epoch = 719468

def to_rata_die(d):
    return d - rata_die_epoch + 1

def from_rata_die(rd):
    return rd + rata_die_epoch - 1

def to_julian_date(d):
    return d - julian_date_epoch

def from_julian_date(jd):
    return jd + julian_date_epoch

def to_lilian_date(d):
    return d - lilian_epoch + 1

def from_lilian_date(ld):
    return ld + lilian_epoch - 1

def to_unix_time(d):
    return 86400 * (d - unix_epoch)

def from_unix_time(ut):
    ud, dt = divmod(ut, 86400)
    return ud + unix_epoch, dt
