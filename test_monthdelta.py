"""Test date/time type.

See http://www.zope.org/Members/fdrake/DateTimeWiki/TestCases
"""

import os
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
from monthdelta import monthdelta, monthmod

pickle_choices = [(pickle, pickle, proto) for proto in range(3)]
assert len(pickle_choices) == 3

# An arbitrary collection of objects of non-datetime types, for testing
# mixed-type comparisons.
OTHERSTUFF = (10, 10, 34.5, "abc", {}, [], ())

class TestMonthDelta(unittest.TestCase):
    expectations = (
        (date(2006,12,31), monthdelta(6),   date(2007,6,30),date(2006,6,30)),
        (date(2007,1,1),   monthdelta(6),   date(2007,7,1), date(2006,7,1)),
        (date(2007,1,2),   monthdelta(6),   date(2007,7,2), date(2006,7,2)),
        (date(2006,12,31), monthdelta(12),date(2007,12,31),date(2005,12,31)),
        (date(2007,1,1),   monthdelta(12),  date(2008,1,1),date(2006,1,1)),
        (date(2007,1,2),   monthdelta(12),  date(2008,1,2),date(2006,1,2)),
        (date(2006,12,31), monthdelta(60),date(2011,12,31),date(2001,12,31)),
        (date(2007,1,1),   monthdelta(60),  date(2012,1,1),date(2002,1,1)),
        (date(2007,1,2),   monthdelta(60),  date(2012,1,2),date(2002,1,2)),
        (date(2006,12,31),monthdelta(600),date(2056,12,31),date(1956,12,31)),
        (date(2007,1,1),   monthdelta(600), date(2057,1,1),date(1957,1,1)),
        (date(2007,1,2),   monthdelta(600), date(2057,1,2),date(1957,1,2)),
        (date(2007,2,27), monthdelta(1), date(2007, 3, 27),date(2007,1, 27)),
        (date(2007,2,28), monthdelta(1), date(2007, 3, 28),date(2007,1, 28)),
        (date(2007,3,1),  monthdelta(1), date(2007, 4, 1), date(2007, 2, 1)),
        (date(2007,3,30), monthdelta(1), date(2007, 4, 30),date(2007,2, 28)),
        (date(2007,3,31), monthdelta(1), date(2007, 4, 30),date(2007,2, 28)),
        (date(2007,4,1),  monthdelta(1), date(2007, 5, 1), date(2007, 3, 1)),
        (date(2008,2,27), monthdelta(1), date(2008, 3, 27),date(2008,1, 27)),
        (date(2008,2,28), monthdelta(1), date(2008, 3, 28),date(2008,1, 28)),
        (date(2008,2,29), monthdelta(1), date(2008, 3, 29),date(2008,1, 29)),
        (date(2008,3,1),  monthdelta(1), date(2008, 4, 1), date(2008, 2, 1)),
        (date(2008,3,30), monthdelta(1), date(2008, 4, 30),date(2008,2, 29)),
        (date(2008,3,31), monthdelta(1), date(2008, 4, 30),date(2008,2, 29)),
        (date(2008,4,1),  monthdelta(1), date(2008, 5, 1), date(2008, 3, 1)),
        (date(2100,2,27), monthdelta(1), date(2100, 3, 27),date(2100,1, 27)),
        (date(2100,2,28), monthdelta(1), date(2100, 3, 28),date(2100,1, 28)),
        (date(2100,3,1),  monthdelta(1), date(2100, 4, 1), date(2100, 2, 1)),
        (date(2100,3,30), monthdelta(1), date(2100, 4, 30),date(2100,2, 28)),
        (date(2100,3,31), monthdelta(1), date(2100, 4, 30),date(2100,2, 28)),
        (date(2100,4,1),  monthdelta(1), date(2100, 5, 1), date(2100, 3, 1)),
        (date(2000,2,27), monthdelta(1), date(2000, 3, 27),date(2000,1, 27)),
        (date(2000,2,28), monthdelta(1), date(2000, 3, 28),date(2000,1, 28)),
        (date(2000,2,29), monthdelta(1), date(2000, 3, 29),date(2000,1, 29)),
        (date(2000,3,1),  monthdelta(1), date(2000, 4, 1), date(2000, 2, 1)),
        (date(2000,3,30), monthdelta(1), date(2000, 4, 30),date(2000,2, 29)),
        (date(2000,3,31), monthdelta(1), date(2000, 4, 30),date(2000,2, 29)),
        (date(2000,4,1),  monthdelta(1), date(2000, 5, 1), date(2000, 3, 1)))

    def test_calc(self):
        for dt, md, sub, prev in self.expectations:
            self.assertEqual(dt + md, sub)
            self.assertEqual(dt - md, prev)
    def test_math(self):
        for x, y in permutations(range(26),2):
            self.assertEqual(monthdelta(x) + monthdelta(y), monthdelta(x +y))
            self.assertEqual(monthdelta(x) - monthdelta(y), monthdelta(x -y))
            self.assertEqual(monthdelta(x) * y, monthdelta(x * y))
        for x, y in combinations(range(26),2):
            self.assertEqual(monthdelta(x) // y, monthdelta(x // y))
            self.assertEqual(monthdelta(x) // monthdelta(y), x // y)
    def test_comp(self):
        for x, y in combinations(range(26),2):
            self.assert_(monthdelta(x) < monthdelta(y))
            self.assert_(monthdelta(x) <= monthdelta(y))
            self.assert_(monthdelta(x) != monthdelta(y))
            self.assert_(monthdelta(y) > monthdelta(x))
            self.assert_(monthdelta(y) >= monthdelta(x))
        for x in range(26):
            self.assert_(monthdelta(x) <= monthdelta(x))
            self.assert_(monthdelta(x) == monthdelta(x))
            self.assert_(monthdelta(x) >= monthdelta(x))
    def test_bool(self):
        self.assert_(monthdelta())
        self.assert_(monthdelta(-1))
        self.assert_(not monthdelta(0))
    def test_class(self):
        self.assertEqual(monthdelta.min, monthdelta(-99999999))
        self.assertEqual(monthdelta.max, monthdelta(99999999))
    def test_subclass(self):
        class M(monthdelta):
            def from_md(md):
                return M(md.months)
            from_md = staticmethod(from_md)
            def as_years(self):
                return round(self.months / 12)

        m1 = M()
        self.assert_(type(m1) is M or type(m1) is types.InstanceType)
        self.assertEqual(m1.as_years(), 0)
        m2 = M(-24)
        self.assert_(type(m2) is M or type(m2) is types.InstanceType)
        self.assertEqual(m2.as_years(), -2)
        m3 = m1 + m2
        self.assert_(type(m3) is monthdelta or type(m3) is types.InstanceType)
        m4 = M.from_md(m3)
        self.assert_(type(m4) is M or type(m4) is types.InstanceType)
        self.assertEqual(m3.months, m4.months)
        self.assertEqual(str(m3), str(m4))
        self.assertEqual(m4.as_years(), -2)
    def test_str(self):
        self.assertEqual(str(monthdelta()), '1 month')
        self.assertEqual(str(monthdelta(-1)), '-1 month')
        self.assertEqual(str(monthdelta(3)), '3 months')
        self.assertEqual(str(monthdelta(-17)), '-17 months')
    def test_pickling(self):
        orig = monthdelta(42)
        green = pickle.dumps(orig)
        derived = pickle.loads(green)
        self.assertEqual(orig, derived)
    def test_disallowed(self):
        a = monthdelta(42)
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
            b = monthdelta(12)
            b //= monthdelta(3)
        self.assertRaises(TypeError, inplace_fail)
        x = 2.3
        self.assertRaises(TypeError, lambda: a*x)
        self.assertRaises(TypeError, lambda: x*a)
        self.assertRaises(TypeError, lambda: a // x)
        self.assertRaises(TypeError, lambda: x // a)
        self.assertRaises(OverflowError, monthdelta, -100000000)
        self.assertRaises(OverflowError, monthdelta, 100000000)

class TestMonthMod(unittest.TestCase):
    md_zero, td_zero = monthdelta(0), timedelta(0)
    expectations = (
        (date(2007,1,1),  date(2007,1,1),  md_zero, td_zero),
        (date(2007,2,28), date(2007,2,28), md_zero, td_zero),
        (date(2007,3,1),  date(2007,3,1),  md_zero, td_zero),
        (date(2008,2,28), date(2008,2,28), md_zero, td_zero),
        (date(2008,2,29), date(2008,2,29), md_zero, td_zero),
        (date(2008,3,1),  date(2008,3,1),  md_zero, td_zero),
        (date(2007,1,1),  date(2007,2,27), monthdelta(1),  timedelta(26)),
        (date(2007,1,1),  date(2007,2,28), monthdelta(1),  timedelta(27)),
        (date(2007,1,1),  date(2007,3,1),  monthdelta(2),  timedelta(0)),
        (date(2007,1,1),  date(2007,3,30), monthdelta(2),  timedelta(29)),
        (date(2007,1,1),  date(2007,3,31), monthdelta(2),  timedelta(30)),
        (date(2007,1,1),  date(2007,4,1),  monthdelta(3),  timedelta(0)),
        (date(2008,1,1),  date(2008,2,27), monthdelta(1),  timedelta(26)),
        (date(2008,1,1),  date(2008,2,28), monthdelta(1),  timedelta(27)),
        (date(2008,1,1),  date(2008,2,29), monthdelta(1),  timedelta(28)),
        (date(2008,1,1),  date(2008,3,1),  monthdelta(2),  timedelta(0)),
        (date(2008,1,1),  date(2008,3,30), monthdelta(2),  timedelta(29)),
        (date(2008,1,1),  date(2008,3,31), monthdelta(2),  timedelta(30)),
        (date(2008,1,1),  date(2008,4,1),  monthdelta(3),  timedelta(0)),
        (date(2006,1,1),  date(2007,2,27), monthdelta(13), timedelta(26)),
        (date(2006,1,1),  date(2007,2,28), monthdelta(13), timedelta(27)),
        (date(2006,1,1),  date(2007,3,1),  monthdelta(14), timedelta(0)),
        (date(2006,1,1),  date(2007,3,30), monthdelta(14), timedelta(29)),
        (date(2006,1,1),  date(2007,3,31), monthdelta(14), timedelta(30)),
        (date(2006,1,1),  date(2007,4,1),  monthdelta(15), timedelta(0)),
        (date(2006,1,1),  date(2008,2,27), monthdelta(25), timedelta(26)),
        (date(2006,1,1),  date(2008,2,28), monthdelta(25), timedelta(27)),
        (date(2006,1,1),  date(2008,2,29), monthdelta(25), timedelta(28)),
        (date(2006,1,1),  date(2008,3,1),  monthdelta(26), timedelta(0)),
        (date(2006,1,1),  date(2008,3,30), monthdelta(26), timedelta(29)),
        (date(2006,1,1),  date(2008,3,31), monthdelta(26), timedelta(30)),
        (date(2006,1,1),  date(2008,4,1),  monthdelta(27), timedelta(0)),
        (date(2007,2,27), date(2007,1,1),  monthdelta(-2), timedelta(5)),
        (date(2007,2,28), date(2007,1,1),  monthdelta(-2), timedelta(4)),
        (date(2007,3,1),  date(2007,1,1),  monthdelta(-2), timedelta(0)),
        (date(2007,3,30), date(2007,1,1),  monthdelta(-3), timedelta(2)),
        (date(2007,3,31), date(2007,1,1),  monthdelta(-3), timedelta(1)),
        (date(2007,4,1),  date(2007,1,1),  monthdelta(-3), timedelta(0)),
        (date(2008,2,27), date(2008,1,1),  monthdelta(-2), timedelta(5)),
        (date(2008,2,28), date(2008,1,1),  monthdelta(-2), timedelta(4)),
        (date(2008,2,29), date(2008,1,1),  monthdelta(-2), timedelta(3)),
        (date(2008,3,1),  date(2008,1,1),  monthdelta(-2), timedelta(0)),
        (date(2008,3,30), date(2008,1,1),  monthdelta(-3), timedelta(2)),
        (date(2008,3,31), date(2008,1,1),  monthdelta(-3), timedelta(1)),
        (date(2008,4,1),  date(2008,1,1),  monthdelta(-3), timedelta(0)),
        (date(2007,2,27), date(2006,1,1),  monthdelta(-14), timedelta(5)),
        (date(2007,2,28), date(2006,1,1),  monthdelta(-14), timedelta(4)),
        (date(2007,3,1),  date(2006,1,1),  monthdelta(-14), timedelta(0)),
        (date(2007,3,30), date(2006,1,1),  monthdelta(-15), timedelta(2)),
        (date(2007,3,31), date(2006,1,1),  monthdelta(-15), timedelta(1)),
        (date(2007,4,1),  date(2006,1,1),  monthdelta(-15), timedelta(0)),
        (date(2008,2,27), date(2006,1,1),  monthdelta(-26), timedelta(5)),
        (date(2008,2,28), date(2006,1,1),  monthdelta(-26), timedelta(4)),
        (date(2008,2,29), date(2006,1,1),  monthdelta(-26), timedelta(3)),
        (date(2008,3,1),  date(2006,1,1),  monthdelta(-26), timedelta(0)),
        (date(2008,3,30), date(2006,1,1),  monthdelta(-27), timedelta(2)),
        (date(2008,3,31), date(2006,1,1),  monthdelta(-27), timedelta(1)),
        (date(2008,4,1),  date(2006,1,1),  monthdelta(-27), timedelta(0)),
        (date.min, date.max-timedelta(365), monthdelta(119975), timedelta(30)))

    def test_calc(self):
        for start, end, md, td in self.expectations:
            self.assertEqual(monthmod(start, end), (md, td))
            self.assert_((start > end and md < self.md_zero) or
                         (start <= end and md >= self.md_zero))
            self.assert_(td >= self.td_zero)
            self.assert_(td < end.replace(end.year+end.month//12,
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
