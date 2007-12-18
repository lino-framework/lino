# posted on 2006-10-03 by a pretty average guy called "bjorn"
# copied from http://blog.tkbe.org/archive/python-how-old-are-you/

from datetime import date as _date
from calendar import monthrange as _monthrange

def age(dob, today=_date.today()):

    y = today.year - dob.year
    m = today.month - dob.month
    d = today.day - dob.day
       
    while m <0 or d <0:
        while m <0:
            y -= 1
            m = 12 + m  # m is negative
        if d <0:
            m -= 1
            days = days_previous_month(today.year, today.month)
            d = max(0, days - dob.day) + today.day
    return y, m, d
       
def days_previous_month(y, m):
    m -= 1
    if m == 0:
        y -= 1
        m = 12
    _, days = _monthrange(y, m)
    return days

