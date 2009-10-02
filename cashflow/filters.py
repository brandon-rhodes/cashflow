"""Filters for processing GnuCash splits."""

# Filters that assign splits to a particular period.

def yearly(transaction, split):
    """Assign a split to a yearly period, like '2008'."""
    split.period = transaction.date_posted[:4]

def quarterly(transaction, split):
    """Assign a split to a quarterly period, like '2008-Q3'."""
    d = transaction.date_posted
    split.period = '%sQ%d' % (d[:5], int(d[5:7]) // 4 + 1)

def monthly(transaction, split):
    """Assign a split to a monthly period, like '2008-09'."""
    split.period = transaction.date_posted[:7]
