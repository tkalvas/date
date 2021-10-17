import core

def is_gregorian(yg, mg, dg):
    """Check if (year, month, day) is a valid Gregorian date."""
    return core.to_gregorian(core.from_gregorian(yg, mg, dg)) == (yg, mg, dg)

def is_iso_week_date(yi, wi, di):
    """Check if (year, week, weekday) is a valid ISO8601 week-format date."""
    return core.to_iso_week_date(core.from_iso_week_date(yi, wi, di)) == (yi, wi, di)
