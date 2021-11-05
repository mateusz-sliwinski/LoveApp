"""Utils.py files."""
# Standard Library
import datetime
from datetime import date

# Django
from django.core.exceptions import ValidationError

# 3rd-party
from dateutil.relativedelta import relativedelta


def time_today():  # noqa D103
    current_date = datetime.date.today()
    print(current_date)
    return current_date


def legitimate_age(birth_date): # noqa D103
    today = date.today()
    age = relativedelta(today, birth_date)

    data = int(age.years)

    if data <= 17:
        raise ValidationError('You pick to young age.')
    return age.years


def validate_tags(list): # noqa D103
    if len(list) > 5:
        raise ValidationError('You take to much tags.')
    return list


def take_id_from_path(full_path): # noqa D103
    reverse_path = full_path[::-1]
    right_id = reverse_path.split('/')

    return right_id[0]
