"""Various reports that can be generated from a GnuCash ledger book."""

from collections import defaultdict
from decimal import Decimal, ROUND_DOWN

one_hundred = Decimal(100) # to avoids creating this thousands of times

def make_int_dict():
    """A dictionary whose default values are (integer) zero."""
    return defaultdict(int)

def get_account_name(accounts, transaction, split):
    a = accounts[split.account_guid]
    if a.type in ('BANK', 'CASH', 'CREDIT'):
        return True
    return a.name

def compute_cashflow(book, key, regular_expenses=[],
                     account_name_getter=get_account_name):
    """Compute where cash has flowed for every month in the ledger book."""
    month_regular = defaultdict(make_int_dict)
    month_expenses = defaultdict(make_int_dict)
    month_income = defaultdict(make_int_dict)

    # Fetch the accounts from inside this GnuCash ledger book.

    accounts = dict( (a.guid, a) for a in book.accounts )

    # Next, we need to determine which accounts count as our cash pool.

    for t in book.transactions:
        k = key(t.date_posted) # like '2008' or '2008-08' or something
        splits = list(t.splits)
        account_names = [ account_name_getter(accounts, t, s)
                          for s in splits ]
        if True in account_names:
            for account_name, split in zip(account_names, splits):
                if account_name is not None and account_name is not True:
                    value = split.value
                    numerator, denominator = value.split('/')
                    if denominator != '100':
                        raise ValueError('cashflow only supports'
                                         ' hundredth-based currencies')
                    ivalue = Decimal(numerator) / one_hundred
                    if ivalue > 0:
                        if account_name in regular_expenses:
                            month_regular[k][account_name] -= ivalue
                        else:
                            month_expenses[k][account_name] -= ivalue
                    elif ivalue < 0:
                        month_income[k][account_name] -= ivalue

    keys = set()
    keys.update(month_regular)
    keys.update(month_expenses)
    keys.update(month_income)
    keys = sorted(keys)

    return keys, month_regular, month_expenses, month_income

class YearlyReport(object):
    def __init__(self, *args, **kw):
        kw['key'] = lambda date_posted: date_posted[:4] # like '2008'
        self.years, self.regular, self.expenses, self.income = \
            compute_cashflow(*args, **kw)

class QuarterlyReport(object):
    def __init__(self, *args, **kw):
        kw['key'] = lambda date_posted: date_posted[:4] \
            + '-Q%d' % ((int(date_posted[5:7])+2)//3) # like '2008-Q4'
        self.years, self.regular, self.expenses, self.income = \
            compute_cashflow(*args, **kw)

class MonthlyReport(object):
    def __init__(self, *args, **kw):
        self.regular_expenses = kw.get('regular_expenses', [])
        kw['key'] = lambda date_posted: date_posted[:7] # like '2008-08'
        self.months, self.regular, self.expenses, self.income = \
            compute_cashflow(*args, **kw)

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
