"""Utils.py files."""
# Standard Library
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


def time_today():  # noqa D103
    current_date = datetime.date.today()
    return current_date


def legitimate_age(birth_date):
    today = date.today()
    age = relativedelta(today, birth_date)

    data = int(age.years)

    if data <= 17:
        raise ValueError

    return age.years
