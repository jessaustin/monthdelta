==========
MonthDelta
==========

A single module, |mod|_, is provided by the |MonthDelta|_ distribution. The
|mod|_ module includes a class, |MD|_, and a function, `monthmod()`_. |MD|_
enables easy month-related calculations with the standard Python date_ and
datetime_ classes from the |DT|_ module. `monthmod()`_ enables round-trip
calculations among |MD|_, date_, datetime_, and timedelta_. Starting with
`version 2.3`_ (when the |DT|_ module was added), |MonthDelta|_ supports all
subsequent versions of Python_ from one codebase.

This library was originally developed as an enhancement to the C implementation
of Python_, to be included directly in the |DT|_ module. That was not seen as a
valuable addition to the standard library, so this "back-ported" Python_ module
is the way to use this functionality.

Documentation_ is available, and the source_ is hosted at Bitbucket_. `Jess
Austin`_ is the author of |MonthDelta|_. |MonthDelta|_ is distributed under
the `MIT license`_.

.. |MonthDelta| replace:: **MonthDelta**
.. |mod| replace:: **monthdelta**
.. _mod: http://packages.python.org/MonthDelta/#module-monthdelta
.. |MD| replace:: MonthDelta
.. _MD: http://packages.python.org/MonthDelta#monthdelta.MonthDelta
.. _`monthmod()`: http://packages.python.org/MonthDelta#monthdelta.monthmod
.. |DT| replace:: **datetime**
.. _DT: http://docs3.python.org/library/datetime.html
.. _date: http://docs3.python.org/library/datetime.html#datetime.date
.. _datetime: http://docs3.python.org/library/datetime.html#datetime.datetime
.. _timedelta: http://docs3.python.org/library/datetime.html#datetime.timedelta
.. _Python: http://python.org
.. _Documentation: http://packages.python.org/MonthDelta
.. _source: https://bitbucket.org/jessaustin/monthdelta
.. _Bitbucket: https://bitbucket.org
.. _`Jess Austin`: mailto:jess.austin@gmail.com
.. _`MIT License`: http://www.opensource.org/licenses/mit-license.php
.. _`version 2.3`: http://www.python.org/download/releases/2.3.7
