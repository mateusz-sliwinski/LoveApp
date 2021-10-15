"""Utils.py files."""
# Standard Library
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

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


def validate_tags(list):
    if len(list) > 5:
        raise ValidationError('You take to much tags.')

    return list