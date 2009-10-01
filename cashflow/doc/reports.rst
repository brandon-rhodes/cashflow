>>> import cashflow
>>> book = cashflow.open(cashflow.sample_file_path())
>>> report = cashflow.MonthlyReport(book)
>>> cashflow.print_running_balance(report)
<BLANKLINE>
                           1.17   Interest
                       2,821.00   Salary
                       ---------
            2,822.17   2,822.17   Income for 1980-01
<BLANKLINE>
                        (125.63)  Groceries
                         (41.18)  Utilities
                       ---------
             (166.81)   (166.81)  Expenses for 1980-01
            ---------
 2,655.36   2,655.36              Total for 1980-01
 ---------
 2,655.36                         Running total after 1980-01
<BLANKLINE>
                           2.30   Interest
                       2,821.00   Salary
                       ---------
            2,823.30   2,823.30   Income for 1980-02
<BLANKLINE>
                        (130.93)  Groceries
                         (48.62)  Utilities
                       ---------
             (179.55)   (179.55)  Expenses for 1980-02
            ---------
 2,643.75   2,643.75              Total for 1980-02
 ---------
 5,299.11                         Running total after 1980-02


>>> report = cashflow.QuarterlyReport(book)
>>> cashflow.print_running_balance(report)
<BLANKLINE>
                           3.47   Interest
                       5,642.00   Salary
                       ---------
            5,645.47   5,645.47   Income for 1980-Q1
<BLANKLINE>
                        (256.56)  Groceries
                         (89.80)  Utilities
                       ---------
             (346.36)   (346.36)  Expenses for 1980-Q1
            ---------
 5,299.11   5,299.11              Total for 1980-Q1
 ---------
 5,299.11                         Running total after 1980-Q1


>>> report = cashflow.YearlyReport(book)
>>> cashflow.print_running_balance(report)
<BLANKLINE>
                           3.47   Interest
                       5,642.00   Salary
                       ---------
            5,645.47   5,645.47   Income for 1980
<BLANKLINE>
                        (256.56)  Groceries
                         (89.80)  Utilities
                       ---------
             (346.36)   (346.36)  Expenses for 1980
            ---------
 5,299.11   5,299.11              Total for 1980
 ---------
 5,299.11                         Running total after 1980
