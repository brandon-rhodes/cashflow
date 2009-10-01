"""Various reports that can be generated from a GnuCash ledger book."""

from cashflow.format import display

def running_balance(report, one_month=None):
    """Format a running balance sheet, given a `MonthlyReport`."""
    rows = []

    months = set()
    months.update(report.expenses)
    months.update(report.regular)
    months.update(report.income)
    months = sorted(months)

    t = 0
    for month in months:
        if one_month is None or month == one_month:
            t2 = 0

            if report.income[month]:
                rows.append(())
                t3 = 0
                for name, total in sorted(report.income[month].items()):
                    if not total: continue
                    rows.append((None, None, total, name))
                    t3 += total
                rows.append((None, None, '-'))
                rows.append((None, t3, t3, 'Income for ' + month))
                t2 += t3

            if report.regular[month]:
                rows.append(())
                t3 = 0
                for name, total in sorted(report.regular[month].items()):
                    if not total: continue
                    rows.append((None, None, total, name))
                    t3 += total
                rows.append((None, None, '-'))
                rows.append((None, t3, t3, 'Regular expenses for ' + month))
                t2 += t3

            if report.expenses[month]:
                rows.append(())
                t3 = 0
                for name, total in sorted(report.expenses[month].items()):
                    if not total: continue
                    rows.append((None, None, total, name))
                    t3 += total
                rows.append((None, None, '-'))
                rows.append((None, t3, t3, 'Expenses for ' + month))
                t2 += t3

            rows.append((None, '-'))
            rows.append((t2, t2, '', 'Total for ' + month))
            t += t2
            rows.append(('-'))
            rows.append((t, '', '', 'Running total after ' + month))

    return rows

def print_running_balance(*args, **kw):
    display(running_balance(*args, **kw))
