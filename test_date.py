import unittest
import core

def is_leap(yg):
    return yg % 400 == 0 or yg % 4 == 0 and yg % 100 != 0

class TestDate(unittest.TestCase):
    def test_exhaustive(self):
        dp = None
        yg, mg, dg = 2001, 1, 1
        yi, wi, di = 2001, 1, 1
        weeks = 52
        while yg < 2401:
            d = core.from_gregorian(yg, mg, dg)
            if dp is not None:
                self.assertEqual(d, dp + 1)
            self.assertEqual(core.to_gregorian(d), (yg, mg, dg))
            self.assertEqual(core.from_iso_week_date(yi, wi, di), d)
            self.assertEqual(core.to_iso_week_date(d), (yi, wi, di))
            dp = d
            if mg == 2 and dg == 28:
                if is_leap(yg):
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

    def assertEaster(self, y, m, d):
        easter = core.easter(y)
        self.assertEqual(core.to_gregorian(easter), (y, m, d))

    def test_easter(self):
        self.assertEaster(1818, 3, 22)
        self.assertEaster(1999, 4, 4)
        self.assertEaster(2000, 4, 23)
        self.assertEaster(2001, 4, 15)
        self.assertEaster(2002, 3, 31)
        self.assertEaster(2008, 3, 23)
        self.assertEaster(2011, 4, 24)
