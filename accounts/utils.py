"""Utils.py files."""
# Standard Library
import datetime
import math
from datetime import date

# Django
from django.core.exceptions import ValidationError

# 3rd-party
from dateutil.relativedelta import relativedelta

# Project
from accounts.models import Preferences


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


def summary_preferences():  # noqa D103
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


def pref_age_min():  # noqa D103
    sum_pref = Preferences.objects.all().count()
    help_list = [0] * 200
    summary = 0
    for x in range(sum_pref):
        get_pref = Preferences.objects.get(id=x + 1).age_min

        help_list[get_pref] += 1

    for x in range(len(help_list)):
        summary += help_list[x] * x

    summary = summary / sum_pref

    return math.floor(summary)


def pref_age_max():  # noqa D103
    sum_pref = sum_preferences()
    help_list = zeros_list()

    for x in range(sum_pref):
        get_pref = Preferences.objects.get(id=x + 1).age_max

        help_list[get_pref] += 1
    summary = 0
    for x in range(len(help_list)):
        summary += help_list[x] * x

    summary = summary / sum_pref

    return math.floor(summary)


def zeros_list():  # noqa D103
    help_list = [0] * 200
    return help_list


def sum_preferences():  # noqa D103
    sum_pref = Preferences.objects.all().count()
    return sum_pref


def pref_gender():  # noqa D103
    sum_all_user_preferences = sum_preferences()
    help_list = [0] * 3

    for x in range(sum_all_user_preferences):
        get_pref = Preferences.objects.get(id=x + 1).sex

        if get_pref == 'Man':
            help_list[0] += 1
        elif get_pref == 'Woman':
            help_list[1] += 1
        elif get_pref == 'Other':
            help_list[2] += 1
    if help_list[0] > help_list[1] and help_list[0] > help_list[2]:
        return 'Man'
    elif help_list[1] > help_list[0] and help_list[1] > help_list[2]:
        return 'Woman'
    elif help_list[2] > help_list[0] and help_list[2] > help_list[1]:
        return 'Other'
    elif help_list[0] == help_list[1]:
        return 'Man and Woman'
    elif help_list[0] == help_list[2]:
        return 'Man and Other'
    elif help_list[1] == help_list[2]:
        return 'Woman and Other'
    else:
        return 'All genders are equal picked'
