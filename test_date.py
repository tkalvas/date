import unittest
import date

def is_leap(yg):
    return yg % 400 == 0 or yg % 4 == 0 and yg % 100 != 0

class TestDate(unittest.TestCase):
    def test_exhaustive(self):
        dp = None
        yg, mg, dg = 2001, 1, 1
        yi, wi, di = 2001, 1, 1
        leap, weeks = False, 52
        while yg < 2401:
            d = date.from_gregorian(yg, mg, dg)
            if dp is not None:
                self.assertEqual(d, dp + 1)
            self.assertEqual(date.to_gregorian(d), (yg, mg, dg))
            self.assertEqual(date.from_iso_week_date(yi, wi, di), d)
            self.assertEqual(date.to_iso_week_date(d), (yi, wi, di))
            dp = d
            if mg == 2 and dg == 28:
                if leap:
                    dg = 29
                else:
                    mg = 3
                    dg = 1
            else:
                dg = dg + 1
                if dg > [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mg]:
                    mg += 1
                    dg = 1
                if mg > 12:
                    yg += 1
                    mg = 1
                    leap = is_leap(yg)
            di += 1
            if di > 7:
                wi += 1
                di = 1
            if wi > weeks:
                yi += 1
                wi = 1
                if (mg, dg) == (12, 29) or (mg, dg) == (12, 30) and is_leap(yi):
                    weeks = 53
                else:
                    weeks = 52
