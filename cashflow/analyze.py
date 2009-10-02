"""Various reports that can be generated from a GnuCash ledger book."""

from decimal import Decimal, ROUND_DOWN
zero = Decimal(0)

class deprecated_MonthlyReport(object):
    # the following old logic should be re-written as a filter:
    def amortize(self, account, value, start, duration):
        bump = Decimal(value) / duration
        bump = bump.quantize(Decimal('.01'), rounding=ROUND_DOWN)
        dive = bump * (duration - 1)
        if account in self.regular_expenses:
            expenses = self.regular
        else:
            expenses = self.expenses
        expenses[start][account] += dive # add, since expenses are <0
        month = start
        for i in range(duration - 1):
            y, m = [ int(n) for n in month.split('-') ]
            month = '%d-%02d' % ((y, m+1) if m < 12 else (y+1,1))
            expenses[month][account] -= bump

cash_account_types = set(['BANK', 'CREDIT'])

def pull_splits(book, *functions):
    """Return a list of every split in a GnuCash ledger book, post-filters.

    The ``book`` should a ``cashflow.book.Book`` instance that has been
    instantiated atop a GnuCash ledger book.  Each split in the book is
    subjected, in turn, to every function defined in the ``functions``
    list.  Finally, a list is returned of the splits whose ``omit``
    value did not wind up being ``True``.

    """
    # Fetch the accounts from inside this GnuCash ledger book.

    accounts = dict( (a.guid, a) for a in book.accounts )

    # Next, we need to determine which accounts count as our cash pool.

    keepers = []

    for transaction in book.transactions:

        # By default, the period is the month, like "2009-10".

        period = transaction.date_posted[:7]

        # Overwrite the generator "transaction.splits" with a literal
        # list of split objects, so that we get the same objects back
        # each time we iterate across it.

        transaction.splits = list(transaction.splits)

        # Annotate every split in this transaction with useful defaults
        # before we let the user process any of its splits.

        for split in transaction.splits:
            split.period = period
            split.category = 'Transactions'
            split.account = accounts[split.account_guid]
            split.account_name = split.account.name
            split.omit = (split.account.type in cash_account_types)

            split.value = - split.value
            if split.value > zero:
                split.category = 'Income'
            elif split.value < zero:
                split.category = 'Expenses'
            else:
                split.omit = True

        # Then, invoke our caller's transforms on each split, and keep
        # the splits that they do not elect to omit.

        for split in transaction.splits:
            for function in functions:
                function(transaction, split)

            if not split.omit:
                keepers.append(split)

    return keepers
