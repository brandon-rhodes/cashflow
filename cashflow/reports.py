"""Various reports that can be generated from a GnuCash ledger book."""

from decimal import Decimal
from itertools import groupby
from operator import itemgetter

from cashflow.format import display

zero = Decimal(0)

def running_balance(splits):
    """Return a running balance report, given some transaction splits.

    The ``splits`` parameter should be an iterable of objects that each
    offer four properties: ``period``, ``category``, ``account_name``,
    and ``value``.  The return value will be a list of tuples, each of
    which specifies one line of a table, and whose items are the fields
    that should make up that row.  An item whose value is ``'-'``
    indicates that a line should be drawn whose width is that of the
    column, to separate a column of numbers from their sum.

    """
    # Turn each split into a tuple, with the more-significant ordering
    # keys listed first; this determines the entire structure of the
    # resulting report.

    tuples = [ (i.period, i.category, i.account_name, i.value)
               for i in splits ]

    # Sort the tuples.

    tuples.sort()

    # Finally, build the report, which is a list of table rows
    # represented as tuples of fields, by grouping the tuples by each
    # concentric level of organization in turn.  Note that a category
    # prefixed by '!' will, of course, be sorted before categories that
    # begin with normal alphabetic characters, but that the '!' will be
    # stripped before its name is displayed; this lets you put Expense
    # and Income before any other categories.  If there is an '!Income'
    # category, then a 'Profit/loss' subtotal is displayed next.

    rows = []

    t = zero
    for period, tuples0 in groupby(tuples, itemgetter(0)):
        t1 = zero
        for category, tuples1 in groupby(tuples0, itemgetter(1)):
            t2 = zero
            rows.append(())
            for account, tuples2 in groupby(tuples1, itemgetter(2)):
                t3 = sum(t[3] for t in tuples2)
                rows.append((None, None, t3, account))
                t2 += t3
            rows.append((None, None, '-'))
            rows.append((None, t2, t2, category.strip('!') + ' for ' + period))
            t1 += t2
            if category == '!Income':
                rows.append((None, '-'))
                rows.append((None, t1, '', 'Profit/loss for ' + period))
        rows.append((None, '-'))
        rows.append((t1, t1, '', 'Total for ' + period))
        t += t1
        rows.append(('-'))
        rows.append((t, '', '', 'Running total after ' + period))

    return rows

def display_running_balance(*args, **kw):
    display(running_balance(*args, **kw))
