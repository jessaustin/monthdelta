:mod:`monthdelta` --- Pythonic Date Calculation with Months
===========================================================

.. module:: monthdelta
   :synopsis: date calculations with months
.. moduleauthor:: Jess Austin <jess.austin@gmail.com>

The :class:`MonthDelta` class and :func:`monthmod` function provide
month-related date functionality.

:class:`MonthDelta` object
--------------------------

.. class:: MonthDelta([months=1])

   The class constructor takes one optional integer argument, *months*, with a
   default value of 1 (one).

   :param months: :func:`integer <int>`

A :class:`MonthDelta` object represents a quantity of months offset from a
:class:`datetime.date` or :class:`datetime.datetime`.  :class:`MonthDelta`
allows date calculations without regard to the different lengths of different
months. A :class:`MonthDelta` object added to a :class:`~datetime.date` object
produces another :class:`~datetime.date` that has the same
:attr:`~datetime.date.day`, with :attr:`~datetime.date.year` and
:attr:`~datetime.date.month` offset by :attr:`monthdelta.months`.  If the
resulting :attr:`~datetime.date.day` would be too large for the resulting
:attr:`~datetime.date.month`, the last day in that month is used instead:

    >>> date(2008, 1, 30) + monthdelta(1)
    datetime.date(2008, 2, 29)
    >>> date(2008, 1, 30) + monthdelta(2)
    datetime.date(2008, 3, 30)

Adding a :class:`MonthDelta` object to a :class:`~datetime.date` or
:class:`~datetime.datetime` object differs from adding a
:class:`~datetime.timedelta` object in that a :class:`~datetime.timedelta`
object represents a fixed number of :attr:`~datetime.timedelta.days`, while the
number of days that a :class:`MonthDelta` object represents depends on the
actual months that it spans when added to the :class:`~datetime.date` or
:class:`~datetime.datetime` object.

:class:`MonthDelta` objects may be added, subtracted, multiplied, and
floor-divided similarly to :class:`~datetime.timedelta` objects.  They may not
be added to :class:`~datetime.timedelta` objects directly, as both classes are
intended to be used directly with :class:`~datetime.date` and
:class:`~datetime.datetime` objects.

Instance attribute:

.. attribute:: monthdelta.months

   Read-only.

Supported operations:

In the following, *mds* are :class:`MonthDeltas <monthdelta>`, *dts* are 
:class:`dates <datetime.date>` or :class:`datetimes <datetime.datetime>`,
and *i* is an :func:`integer <int>`.

+----------------------+-----------------------------------------------------+
| Operation            | Result                                              |
+======================+=====================================================+
| ``md1 = md2 + md3``  | Sum of *md2* and *md3*. Afterwards                  |
|                      | ``md1 - md2 == md3`` and ``md1 - md3 == md2`` are   |
|                      | :const:`True`. (1)                                  |
+----------------------+-----------------------------------------------------+
| ``md1 = md2 - md3``  | Difference of *md2* and *md3*. Afterwards           |
|                      | ``md1 == md2 - md3`` and ``md2 == md1 + md3`` are   |
|                      | :const:`True`. (1)                                  |
+----------------------+-----------------------------------------------------+
| ``dt2 = dt1 + md``   | *dt2* has all attributes other than                 |
|                      | :attr:`~datetime.datetime.year` and                 |
|                      | :attr:`~datetime.datetime.month` equal to those of  |
|                      | *dt1*, :attr:`~monthdelta.months` months later than |
|                      | *dt1*. (1) (2)                                      |
+----------------------+-----------------------------------------------------+
| ``dt2 = dt1 - md``   | *dt2* has all attributes other than                 |
|                      | :attr:`~datetime.datetime.year` and                 |
|                      | :attr:`~datetime.datetime.month` equal to those of  |
|                      | *dt1*, :attr:`monthdelta.months` months earlier     |
|                      | than *dt1*. (1) (2)                                 |
+----------------------+-----------------------------------------------------+
| ``md1 = md2 * i`` or | Product of *md2* and *i*. Afterwards                |
| ``md1 = i * md2``    | ``md1 // i == md2`` is true, provided ``i != 0``.   |
|                      | Also, ``md1 // md2 == i`` is true, provided         |
|                      | ``md2.months != 0``. (1)                            |
+----------------------+-----------------------------------------------------+
| ``md1 = md2 // i``   | The floor is computed and the remainder (if any) is |
|                      | thrown away. (3)                                    |
+----------------------+-----------------------------------------------------+
| ``i = md2 // md3``   | The floor is computed and the remainder (if any) is |
|                      | thrown away. (3)                                    |
+----------------------+-----------------------------------------------------+
| ``+md1``             | Returns a :class:`MonthDelta` object with the same  |
|                      | value. (4)                                          |
+----------------------+-----------------------------------------------------+
| ``-md1``             | Equivalent to ``monthdelta(-m1.months)``, and to    |
|                      | ``m1 * -1``. (4)                                    |
+----------------------+-----------------------------------------------------+
| ``abs(md1)``         | equivalent to ``+m1`` when ``m1.months >= 0``, and  |
|                      | to ``-m1`` when ``m1.months < 0``. (4)              |
+----------------------+-----------------------------------------------------+

Notes:

(1)
   May overflow.
(2)
   When the resulting :class:`~datetime.date` would have too large a
   :attr:`~datetime.date.day` for its :attr:`~datetime.date.month`, it has the
   last day of that month:

   >>> date(2008,1,30) + monthdelta(1)
   date(2008,2,29)

   :class:`MonthDelta` calculations involving the 29th, 30th, and 31st days
   of the month are not necessarily invertible:
  
   >>> date(2008,2,29) - monthdelta(1)
   date(2008,1,29)

   When the resulting :class:`~datetime.datetime` has its
   :attr:`~datetime.datetime.day` moved to the last day of the month, the
   :attr:`~datetime.datetime.hour`, :attr:`~datetime.datetime.minute`,
   :attr:`~datetime.datetime.second`, :attr:`~datetime.datetime.microsecond`,
   and :attr:`~datetime.datetime.tzinfo` attributes are not changed:

   >>> datetime(2008, 1, 30, 12, 30, 13) + monthdelta(1)
   datetime.datetime(2008, 2, 29, 12, 30, 13)

   Adding or subtracting a :class:`~datetime.date` object and a
   :class:`MonthDelta` object produces another :class:`~datetime.date` object.
   Use the :func:`monthmod` function in order to produce a :class:`MonthDelta`
   object from two :class:`~datetime.date` objects.

   Adding or subtracting a :class:`~datetime.datetime` object and a
   :class:`MonthDelta` object produces another :class:`~datetime.datetime`.
   Use the :func:`monthmod` function in order to produce a :class:`MonthDelta`
   object from two :class:`~datetime.datetime` objects.
(3)
   Division by 0 raises :exc:`ZeroDivisionError`.
(4)
   Cannot overflow.

Comparisons of :class:`MonthDelta` objects are supported; the object with the
lesser :attr:`~monthdelta.months` attribute is considered the lesser
:class:`MonthDelta`.

:class:`MonthDelta` objects are *hashable* and support efficient pickling. In
Boolean contexts, a :class:`MonthDelta` object is considered to be
:const:`True` if and only if it isn't equal to ``monthdelta(0)``.

Example usage:

   >>> date(2008, 1, 1) + monthdelta(1)
   datetime.date(2008, 2, 1)
   >>> date(2008, 1, 30) + monthdelta(1)
   datetime.date(2008, 2, 29)
   >>> date(2008, 1, 31) + monthdelta(1)
   datetime.date(2008, 2, 29)
   >>> date(2008, 1, 31) + monthdelta(6)
   datetime.date(2008, 7, 31)
   >>> year = monthdelta(12)
   >>> date(2008, 2, 29) + year
   datetime.date(2009, 2, 28)
   >>> date(2008, 2, 29) + 4*year
   datetime.date(2012, 2, 29)

Example of working with :class:`~datetime.date` and :class:`MonthDelta`.  We
have a dictionary of accounts associated with sorted lists of their invoice
dates, and we're looking for missing invoices:

   >>> invoices = {123: [date(2008, 1, 31),
   ...                   date(2008, 2, 29),
   ...                   date(2008, 3, 31),
   ...                   date(2008, 4, 30),
   ...                   date(2008, 5, 31),
   ...                   date(2008, 6, 30),
   ...                   date(2008, 7, 31),
   ...                   date(2008, 12, 31)],
   ...             456: [date(2008, 1, 1),
   ...                   date(2008, 5, 1),
   ...                   date(2008, 6, 1),
   ...                   date(2008, 7, 1),
   ...                   date(2008, 8, 1),
   ...                   date(2008, 11, 1),
   ...                   date(2008, 12, 1)]}
   >>> for account, dates in invoices.items():
   ...     a = dates[0]
   ...     for b in dates[1:]:
   ...         if b - monthdelta(1) > a:
   ...             print('account', account, 'missing between', a, 'and', b)
   ...         a = b
   ...
   account 456 missing between 2008-01-01 and 2008-05-01
   account 456 missing between 2008-08-01 and 2008-11-01
   account 123 missing between 2008-07-31 and 2008-12-31


:func:`monthmod` function
-------------------------

.. function:: monthmod(start, end)

   Return the interim between ``start`` and ``end``, distributed into a
   "months" portion and a remainder.

   :param start: :class:`~datetime.date`
   :param end: :class:`~datetime.date`
   :rtype: (:class:`MonthDelta`, :class:`~datetime.timedelta`) tuple

``start`` and ``end`` must support mutual subtraction.  For this reason,
passing a :class:`~datetime.date` object and a :class:`~datetime.datetime`
object together will raise a :py:exc:`TypeError`.  Subclasses that override
:func:`__sub__` could work, however.

If and only if ``start`` is greater than ``end``, returned
:class:`MonthDelta` is negative.  Returned :class:`~datetime.timedelta` is
never negative, and its :attr:`~datetime.timedelta.days` attribute is always
less than the number of days in ``end.month``.
    
   **Invariant:** ``dt + monthmod(dt, dt+td)[0] + monthmod(dt, dt+td)[1]
   == dt + td`` is :const:`True`.

:func:`monthmod` allows round-trip :class:`~datetime.date` calculations
involving :class:`MonthDelta` and :class:`~datetime.timedelta` objects:

   >>> monthmod(date(2008, 1, 14), date(2009, 4, 2))
   (datetime.monthdelta(14), datetime.timedelta(19))
   >>> date(2008, 1, 14) + _[0] + _[1]
   datetime.date(2009, 4, 2)
   >>> monthmod(date(2009, 4, 2), date(2008, 1, 14))
   (datetime.monthdelta(-15), datetime.timedelta(12))
   >>> date(2009, 4, 2) + _[0] + _[1]
   datetime.date(2008, 1, 14)

