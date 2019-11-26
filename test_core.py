import unittest
import core
import step
from itertools import islice

class TestDate(unittest.TestCase):
    def test_exhaustive(self):
        dp = 730790
        for g, w, in islice(zip(step.generate_gregorian(dp + 1),
                                step.generate_iso_week_date(dp + 1)),
                            0, 146097):
            self.assertEqual(g.day, dp + 1)
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
            dp = g.day

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
