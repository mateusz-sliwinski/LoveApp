"""Utils.py files."""
# Standard Library
import datetime
from datetime import date

# Django
from django.core.exceptions import ValidationError

# 3rd-party
from dateutil.relativedelta import relativedelta
from django.db.models import Count

from accounts.models import CustomUser, Preferences


def time_today():  # noqa D103
    current_date = datetime.date.today()
    return current_date


def legitimate_age(birth_date):  # noqa D103
    today = date.today()
    age = relativedelta(today, birth_date)

    data = int(age.years)

    if data <= 17:
        raise ValidationError('You pick to young age.')
    return age.years


def validate_tags(list):  # noqa D103
    if len(list) > 5:
        raise ValidationError('You take to much tags.')
    return list


def take_id_from_path(full_path):  # noqa D103
    reverse_path = full_path[::-1]
    right_id = reverse_path.split('/')

    return right_id[0]


def summary_preferences():
    sum_pref = Preferences.objects.all().count()
    help_list = [0] * 6
    for x in range(sum_pref):
        get_pref = Preferences.objects.get(id=x + 1).tags

        for y in range(len(get_pref)):
            if get_pref[y] == 'Netflix & Chill':
                help_list[0] += 1
            elif get_pref[y] == 'Books':
                help_list[1] += 1
            elif get_pref[y] == 'Travels':
                help_list[2] += 1
            elif get_pref[y] == 'Going out for wine':
                help_list[3] += 1
            elif get_pref[y] == 'Diner':
                help_list[4] += 1
            elif get_pref[y] == 'Model bonding':
                help_list[5] += 1

    return help_list

