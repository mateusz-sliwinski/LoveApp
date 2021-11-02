"""Utils.py files."""
from random import randint

from accounts.models import PhotoUser, Preferences


def randomize(all_users_count, actually_user):
    while True:
        x = randint(1, all_users_count)
        if x != actually_user:
            break

    return x


def person_and_tags(all_photo, context, current_user_id):
    random = randomize(all_photo, current_user_id)
    context['picture'] = PhotoUser.objects.filter(custom_user=random).all()
    context['preferences'] = Preferences.objects.filter(custom_user=random).all()
    context = {
        'preferences': context['preferences'],
        'picture': context['picture'],
    }
    return context
