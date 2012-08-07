# Test MonthDelta() class and monthmod() function.
#
# See http://www.zope.org/Members/fdrake/DateTimeWiki/TestCases

import pickle
import unittest
import types

from operator import lt, le, gt, ge, eq, ne

try:
    reversed
    sorted
except NameError:
    def reversed(seq):
        return seq[::-1]
    def sorted(it):
        it = list(it)
        it.sort()
        return it
try:
    from test import support
except ImportError:
    from test import test_support as support
try:
    from itertools import combinations, permutations
except ImportError:
    def permutations(iterable, r=None):
        pool = tuple(iterable)
        n = len(pool)
        if r is None:
            r = n
        indices = range(n)
        cycles = range(n, n-r, -1)
        yield tuple([pool[i] for i in indices[:r]])
        while n:
            for i in reversed(range(r)):
                cycles[i] -= 1
                if cycles[i] == 0:
                    indices[i:] = indices[i+1:] + indices[i:i+1]
                    cycles[i] = n - i
                else:
                    j = cycles[i]
                    indices[i], indices[-j] = indices[-j], indices[i]
                    yield tuple([pool[i] for i in indices[:r]])
                    break
            else:
                return
    def combinations(iterable, r):
        pool = tuple(iterable)
        n = len(pool)
        for indices in permutations(range(n), r):
            if sorted(indices) == list(indices):
                yield tuple([pool[i] for i in indices])

from datetime import MINYEAR, MAXYEAR
from datetime import timedelta
from datetime import tzinfo
from datetime import time
from datetime import date, datetime
from monthdelta import MonthDelta, monthmod

pickle_choices = [(pickle, pickle, proto) for proto in range(3)]
assert len(pickle_choices) == 3

# An arbitrary collection of objects of non-datetime types, for testing
# mixed-type comparisons.
OTHERSTUFF = (10, 10, 34.5, "abc", {}, [], ())

class TestMonthDelta(unittest.TestCase):
    expectations = (
        (date(2006,12,31), MonthDelta(6),   date(2007,6,30),date(2006,6,30)),
        (date(2007,1,1),   MonthDelta(6),   date(2007,7,1), date(2006,7,1)),
        (date(2007,1,2),   MonthDelta(6),   date(2007,7,2), date(2006,7,2)),
        (date(2006,12,31), MonthDelta(12),date(2007,12,31),date(2005,12,31)),
        (date(2007,1,1),   MonthDelta(12),  date(2008,1,1),date(2006,1,1)),
        (date(2007,1,2),   MonthDelta(12),  date(2008,1,2),date(2006,1,2)),
        (date(2006,12,31), MonthDelta(60),date(2011,12,31),date(2001,12,31)),
        (date(2007,1,1),   MonthDelta(60),  date(2012,1,1),date(2002,1,1)),
        (date(2007,1,2),   MonthDelta(60),  date(2012,1,2),date(2002,1,2)),
        (date(2006,12,31), MonthDelta(600),date(2056,12,31),date(1956,12,31)),
        (date(2007,1,1),   MonthDelta(600), date(2057,1,1),date(1957,1,1)),
        (date(2007,1,2),   MonthDelta(600), date(2057,1,2),date(1957,1,2)),
        (date(2007,2,27),  MonthDelta(1), date(2007, 3, 27),date(2007,1, 27)),
        (date(2007,2,28),  MonthDelta(1), date(2007, 3, 28),date(2007,1, 28)),
        (date(2007,3,1),   MonthDelta(1), date(2007, 4, 1), date(2007, 2, 1)),
        (date(2007,3,30),  MonthDelta(1), date(2007, 4, 30),date(2007,2, 28)),
        (date(2007,3,31),  MonthDelta(1), date(2007, 4, 30),date(2007,2, 28)),
        (date(2007,4,1),   MonthDelta(1), date(2007, 5, 1), date(2007, 3, 1)),
        (date(2008,2,27),  MonthDelta(1), date(2008, 3, 27),date(2008,1, 27)),
        (date(2008,2,28),  MonthDelta(1), date(2008, 3, 28),date(2008,1, 28)),
        (date(2008,2,29),  MonthDelta(1), date(2008, 3, 29),date(2008,1, 29)),
        (date(2008,3,1),   MonthDelta(1), date(2008, 4, 1), date(2008, 2, 1)),
        (date(2008,3,30),  MonthDelta(1), date(2008, 4, 30),date(2008,2, 29)),
        (date(2008,3,31),  MonthDelta(1), date(2008, 4, 30),date(2008,2, 29)),
        (date(2008,4,1),   MonthDelta(1), date(2008, 5, 1), date(2008, 3, 1)),
        (date(2100,2,27),  MonthDelta(1), date(2100, 3, 27),date(2100,1, 27)),
        (date(2100,2,28),  MonthDelta(1), date(2100, 3, 28),date(2100,1, 28)),
        (date(2100,3,1),   MonthDelta(1), date(2100, 4, 1), date(2100, 2, 1)),
        (date(2100,3,30),  MonthDelta(1), date(2100, 4, 30),date(2100,2, 28)),
        (date(2100,3,31),  MonthDelta(1), date(2100, 4, 30),date(2100,2, 28)),
        (date(2100,4,1),   MonthDelta(1), date(2100, 5, 1), date(2100, 3, 1)),
        (date(2000,2,27),  MonthDelta(1), date(2000, 3, 27),date(2000,1, 27)),
        (date(2000,2,28),  MonthDelta(1), date(2000, 3, 28),date(2000,1, 28)),
        (date(2000,2,29),  MonthDelta(1), date(2000, 3, 29),date(2000,1, 29)),
        (date(2000,3,1),   MonthDelta(1), date(2000, 4, 1), date(2000, 2, 1)),
        (date(2000,3,30),  MonthDelta(1), date(2000, 4, 30),date(2000,2, 29)),
        (date(2000,3,31),  MonthDelta(1), date(2000, 4, 30),date(2000,2, 29)),
        (date(2000,4,1),   MonthDelta(1), date(2000, 5, 1), date(2000, 3, 1)))

    def test_calc(self):
        for dt, md, sub, prev in self.expectations:
            self.assertEqual(dt + md, sub)
            self.assertEqual(dt - md, prev)
    def test_math(self):
        for x, y in permutations(range(26),2):
            self.assertEqual(MonthDelta(x) + MonthDelta(y), MonthDelta(x +y))
            self.assertEqual(MonthDelta(x) - MonthDelta(y), MonthDelta(x -y))
            self.assertEqual(MonthDelta(x) * y, MonthDelta(x * y))
        for x, y in combinations(range(26),2):
            self.assertEqual(MonthDelta(x) // y, MonthDelta(x // y))
            self.assertEqual(MonthDelta(x) // MonthDelta(y), x // y)
    def test_comp(self):
        for x, y in combinations(range(26),2):
            self.assertTrue(MonthDelta(x) < MonthDelta(y))
            self.assertTrue(MonthDelta(x) <= MonthDelta(y))
            self.assertTrue(MonthDelta(x) != MonthDelta(y))
            self.assertTrue(MonthDelta(y) > MonthDelta(x))
            self.assertTrue(MonthDelta(y) >= MonthDelta(x))
        for x in range(26):
            self.assertTrue(MonthDelta(x) <= MonthDelta(x))
            self.assertTrue(MonthDelta(x) == MonthDelta(x))
            self.assertTrue(MonthDelta(x) >= MonthDelta(x))
    def test_bool(self):
        self.assertTrue(MonthDelta())
        self.assertTrue(MonthDelta(-1))
        self.assertTrue(not MonthDelta(0))
    def test_subclass(self):
        class M(MonthDelta):
            def from_md(md):
                return M(md.months)
            from_md = staticmethod(from_md)
            def as_years(self):
                return round(self.months / 12)

        m1 = M()
        self.assertTrue(type(m1) is M or type(m1) is types.InstanceType)
        self.assertEqual(m1.as_years(), 0)
        m2 = M(-24)
        self.assertTrue(type(m2) is M or type(m2) is types.InstanceType)
        self.assertEqual(m2.as_years(), -2)
        m3 = m1 + m2
        self.assertTrue(type(m3) is MonthDelta or
                        type(m3) is types.InstanceType)
        m4 = M.from_md(m3)
        self.assertTrue(type(m4) is M or type(m4) is types.InstanceType)
        self.assertEqual(m3.months, m4.months)
        self.assertEqual(str(m3), str(m4))
        self.assertEqual(m4.as_years(), -2)
    def test_str(self):
        self.assertEqual(str(MonthDelta()), '1 month')
        self.assertEqual(str(MonthDelta(-1)), '-1 month')
        self.assertEqual(str(MonthDelta(3)), '3 months')
        self.assertEqual(str(MonthDelta(-17)), '-17 months')
    def test_pickling(self):
        orig = MonthDelta(42)
        green = pickle.dumps(orig)
        derived = pickle.loads(green)
        self.assertEqual(orig, derived)
    def test_disallowed(self):
        a = MonthDelta(42)
        for i in 1, 1.0:
            self.assertRaises(TypeError, lambda: a+i)
            self.assertRaises(TypeError, lambda: a-i)
            self.assertRaises(TypeError, lambda: i+a)
            self.assertRaises(TypeError, lambda: i-a)
            self.assertRaises(TypeError, lambda: a/i)
            self.assertRaises(TypeError, lambda: i/a)
            self.assertRaises(TypeError, lambda: a/a)
            self.assertRaises(ZeroDivisionError, lambda: a // 0)
        def inplace_fail():
            b = MonthDelta(12)
            b //= MonthDelta(3)
        self.assertRaises(TypeError, inplace_fail)
        x = 2.3
        self.assertRaises(TypeError, lambda: a*x)
        self.assertRaises(TypeError, lambda: x*a)
        self.assertRaises(TypeError, lambda: a // x)
        self.assertRaises(TypeError, lambda: x // a)

class TestMonthMod(unittest.TestCase):
    md_zero, td_zero = MonthDelta(0), timedelta(0)
    expectations = (
        (date(2007,1,1),  date(2007,1,1),  md_zero, td_zero),
        (date(2007,2,28), date(2007,2,28), md_zero, td_zero),
        (date(2007,3,1),  date(2007,3,1),  md_zero, td_zero),
        (date(2008,2,28), date(2008,2,28), md_zero, td_zero),
        (date(2008,2,29), date(2008,2,29), md_zero, td_zero),
        (date(2008,3,1),  date(2008,3,1),  md_zero, td_zero),
        (date(2007,1,1),  date(2007,2,27), MonthDelta(1),  timedelta(26)),
        (date(2007,1,1),  date(2007,2,28), MonthDelta(1),  timedelta(27)),
        (date(2007,1,1),  date(2007,3,1),  MonthDelta(2),  timedelta(0)),
        (date(2007,1,1),  date(2007,3,30), MonthDelta(2),  timedelta(29)),
        (date(2007,1,1),  date(2007,3,31), MonthDelta(2),  timedelta(30)),
        (date(2007,1,1),  date(2007,4,1),  MonthDelta(3),  timedelta(0)),
        (date(2008,1,1),  date(2008,2,27), MonthDelta(1),  timedelta(26)),
        (date(2008,1,1),  date(2008,2,28), MonthDelta(1),  timedelta(27)),
        (date(2008,1,1),  date(2008,2,29), MonthDelta(1),  timedelta(28)),
        (date(2008,1,1),  date(2008,3,1),  MonthDelta(2),  timedelta(0)),
        (date(2008,1,1),  date(2008,3,30), MonthDelta(2),  timedelta(29)),
        (date(2008,1,1),  date(2008,3,31), MonthDelta(2),  timedelta(30)),
        (date(2008,1,1),  date(2008,4,1),  MonthDelta(3),  timedelta(0)),
        (date(2006,1,1),  date(2007,2,27), MonthDelta(13), timedelta(26)),
        (date(2006,1,1),  date(2007,2,28), MonthDelta(13), timedelta(27)),
        (date(2006,1,1),  date(2007,3,1),  MonthDelta(14), timedelta(0)),
        (date(2006,1,1),  date(2007,3,30), MonthDelta(14), timedelta(29)),
        (date(2006,1,1),  date(2007,3,31), MonthDelta(14), timedelta(30)),
        (date(2006,1,1),  date(2007,4,1),  MonthDelta(15), timedelta(0)),
        (date(2006,1,1),  date(2008,2,27), MonthDelta(25), timedelta(26)),
        (date(2006,1,1),  date(2008,2,28), MonthDelta(25), timedelta(27)),
        (date(2006,1,1),  date(2008,2,29), MonthDelta(25), timedelta(28)),
        (date(2006,1,1),  date(2008,3,1),  MonthDelta(26), timedelta(0)),
        (date(2006,1,1),  date(2008,3,30), MonthDelta(26), timedelta(29)),
        (date(2006,1,1),  date(2008,3,31), MonthDelta(26), timedelta(30)),
        (date(2006,1,1),  date(2008,4,1),  MonthDelta(27), timedelta(0)),
        (date(2007,2,27), date(2007,1,1),  MonthDelta(-2), timedelta(5)),
        (date(2007,2,28), date(2007,1,1),  MonthDelta(-2), timedelta(4)),
        (date(2007,3,1),  date(2007,1,1),  MonthDelta(-2), timedelta(0)),
        (date(2007,3,30), date(2007,1,1),  MonthDelta(-3), timedelta(2)),
        (date(2007,3,31), date(2007,1,1),  MonthDelta(-3), timedelta(1)),
        (date(2007,4,1),  date(2007,1,1),  MonthDelta(-3), timedelta(0)),
        (date(2008,2,27), date(2008,1,1),  MonthDelta(-2), timedelta(5)),
        (date(2008,2,28), date(2008,1,1),  MonthDelta(-2), timedelta(4)),
        (date(2008,2,29), date(2008,1,1),  MonthDelta(-2), timedelta(3)),
        (date(2008,3,1),  date(2008,1,1),  MonthDelta(-2), timedelta(0)),
        (date(2008,3,30), date(2008,1,1),  MonthDelta(-3), timedelta(2)),
        (date(2008,3,31), date(2008,1,1),  MonthDelta(-3), timedelta(1)),
        (date(2008,4,1),  date(2008,1,1),  MonthDelta(-3), timedelta(0)),
        (date(2007,2,27), date(2006,1,1),  MonthDelta(-14), timedelta(5)),
        (date(2007,2,28), date(2006,1,1),  MonthDelta(-14), timedelta(4)),
        (date(2007,3,1),  date(2006,1,1),  MonthDelta(-14), timedelta(0)),
        (date(2007,3,30), date(2006,1,1),  MonthDelta(-15), timedelta(2)),
        (date(2007,3,31), date(2006,1,1),  MonthDelta(-15), timedelta(1)),
        (date(2007,4,1),  date(2006,1,1),  MonthDelta(-15), timedelta(0)),
        (date(2008,2,27), date(2006,1,1),  MonthDelta(-26), timedelta(5)),
        (date(2008,2,28), date(2006,1,1),  MonthDelta(-26), timedelta(4)),
        (date(2008,2,29), date(2006,1,1),  MonthDelta(-26), timedelta(3)),
        (date(2008,3,1),  date(2006,1,1),  MonthDelta(-26), timedelta(0)),
        (date(2008,3,30), date(2006,1,1),  MonthDelta(-27), timedelta(2)),
        (date(2008,3,31), date(2006,1,1),  MonthDelta(-27), timedelta(1)),
        (date(2008,4,1),  date(2006,1,1),  MonthDelta(-27), timedelta(0)),
        (date.min, date.max-timedelta(365), MonthDelta(119975), timedelta(30)))

    def test_calc(self):
        for start, end, md, td in self.expectations:
            self.assertEqual(monthmod(start, end), (md, td))
            self.assertTrue((start > end and md < self.md_zero) or
                            (start <= end and md >= self.md_zero))
            self.assertTrue(td >= self.td_zero)
            self.assertTrue(td < end.replace(end.year+end.month//12,
                                          end.month%12+1, 1) -
                              end.replace(day=1))
    def test_invariant(self):
        for start, end, md, td in self.expectations:
            self.assertEqual(sum(monthmod(start, start + td), start),
                             start + td)
            self.assertEqual(sum(monthmod(end, end + td), end),
                             end + td)

    def test_error_handling(self):
        self.assertRaises(TypeError, monthmod, date.min)
        self.assertRaises(TypeError, monthmod, 123, 'abc')
        self.assertRaises(TypeError, monthmod, end=date.max)
        self.assertRaises(TypeError, monthmod, date.min, datetime.max)
        self.assertRaises(TypeError, monthmod, datetime.min, date.max)
        # perhaps it would be better not to overflow for this, but we rely on
        # the addition defined by the type of the arguments
        self.assertRaises(OverflowError, monthmod, date.min+timedelta(1),
                                                   date.min)

def test_main():
    support.run_unittest(TestMonthDelta, TestMonthMod)

if __name__ == "__main__":
    test_main()
