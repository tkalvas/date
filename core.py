week_epoch = -58

def divmoddiv(a, b, c):
    i, j = divmod(a, b)
    return i, j // c

def from_gregorian(yg, mg, dg):
    y, my = divmod(12*yg + mg - 3, 12)
    dy = (153*my + 2)//5 + dg - 1
    return 365*y + y//4 - y//100 + y//400 + dy

def to_gregorian(d):
    y, dy = divmoddiv((d + (4*d + 146101)//146097*3//4) * 4 + 3, 1461, 4)
    my, dm = divmoddiv(5*dy + 2, 153, 5)
    yg, mg0 = divmod(12*y + my + 2, 12)
    return yg, mg0 + 1, dm + 1

def from_iso_week_date(yi, wi, di):
    w = (1461*yi + 7 - 4*((yi - 1)//100 - yi//400)) // 28 + wi - 1
    return 7*w + di - 1 + week_epoch

def to_iso_week_date(d):
    w, dw = divmod(d - week_epoch, 7)
    yi, wy = divmoddiv(28*w + 20 - 4*(5269 - w)//20871*3//4*4, 1461, 28)
    return yi, wy + 1, dw + 1

