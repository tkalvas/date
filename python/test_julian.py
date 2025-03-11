import unittest
import core
import julian
import epoch
import step
from itertools import count, islice

class TestJulian(unittest.TestCase):
    def test_exhaustive(self):
        base = 730791
        for j, d in islice(zip(step.generate_julian(base),
                               count(base)),
                           0, 146097):
            self.assertEqual(j.day, d)
            self.assertEqual(julian.to_julian(j.day),
                             (j.year, j.month, j.day_of_month))
            self.assertEqual(julian.from_julian(j.year, j.month, j.day_of_month),
                             j.day)

    def test_1582(self):
        from_day = julian.from_julian(1582, 10, 4)
        to_day = core.from_gregorian(1582, 10, 15)
        self.assertEqual(from_day + 1, to_day)

    def test_bc_ad(self):
        from_day = julian.from_julian(-1, 12, 31)
        to_day = julian.from_julian(1, 1, 1)
        self.assertEqual(from_day + 1, to_day)
        self.assertEqual(julian.to_julian(from_day), (-1, 12, 31))
        self.assertEqual(julian.to_julian(to_day), (1, 1, 1))

    def test_4713(self):
        self.assertEqual(julian.to_julian(int(epoch.from_julian_date(-0.5))),
                         (-4713, 1, 1))
