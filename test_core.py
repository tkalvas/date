import unittest
import core
import step
from itertools import count, islice

class TestDate(unittest.TestCase):
    def test_exhaustive(self):
        base = 730791
        for g, w, d in islice(zip(step.generate_gregorian(base),
                                  step.generate_iso_week_date(base),
                                  count(base)),
                              0, 146097):
            self.assertEqual(g.day, d)
            self.assertEqual(g.day, w.day)
            self.assertEqual(g.weekday + 1, w.day_of_week)
            self.assertEqual(core.to_gregorian(g.day),
                             (g.year, g.month, g.day_of_month))
            self.assertEqual(core.from_gregorian(g.year, g.month,
                                                 g.day_of_month),
                             g.day)
            self.assertEqual(core.to_iso_week_date(w.day),
                             (w.year, w.week, w.day_of_week))
            self.assertEqual(core.from_iso_week_date(w.year, w.week,
                                                     w.day_of_week),
                             w.day)

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
        self.assertEaster(2049, 4, 18)

    def test_ceiling_weekday(self):
        for wd in range(0, 7):
            for d in range(0, 14):
                r = core.ceiling_weekday(d, wd)
                self.assertGreaterEqual(r, d)
                self.assertLess(r, d + 7)
                self.assertEqual(wd, core.weekday(r))

    def test_next_weekday(self):
        for wd in range(0, 7):
            for d in range(0, 14):
                r = core.next_weekday(d, wd)
                self.assertGreater(r, d)
                self.assertLessEqual(r, d + 7)
                self.assertEqual(wd, core.weekday(r))

    def test_previous_weekday(self):
        for wd in range(0, 7):
            for d in range(0, 14):
                r = core.previous_weekday(d, wd)
                self.assertGreaterEqual(r, d - 7)
                self.assertLess(r, d)
                self.assertEqual(wd, core.weekday(r))

    def test_floor_weekday(self):
        for wd in range(0, 7):
            for d in range(0, 14):
                r = core.floor_weekday(d, wd)
                self.assertGreater(r, d - 7)
                self.assertLessEqual(r, d)
                self.assertEqual(wd, core.weekday(r))
