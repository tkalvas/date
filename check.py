import core

def is_gregorian(yg, mg, dg):
    return core.to_gregorian(core.from_gregorian(yg, mg, dg)) == (yg, mg, dg)

def is_iso_week_date(yi, wi, di):
    return core.to_iso_week_date(core.from_iso_week_date(yi, wi, di)) == (yi, wi, di)
