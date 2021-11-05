"""Utils.py files."""
from random import randint

from accounts.models import PhotoUser, Preferences, CustomUser
from core.models import Likes


def randomize(all_users_count, actually_user):
    while True:
        x = randint(1, all_users_count)
        if x != actually_user:
            break

    return x


def person_and_tags(all_photo, context, current_user_id):
    random = randomize(all_photo, current_user_id)
    context = take_context(context, random)
    return context


def person_and_tags_for_like(all_photo, context, current_user_id, current_user):
    random = randomize(all_photo, current_user_id)
    context = take_context(context, random)

    x = Likes.objects.create(
        user_one=current_user,
        user_two=CustomUser.objects.get(id=random),
        status='NUll',
    )
    x.save()

    return context


def take_context(context, random):
    context['picture'] = PhotoUser.objects.filter(custom_user=random).all()
    context['preferences'] = Preferences.objects.filter(custom_user=random).all()
    context = {
        'preferences': context['preferences'],
        'picture': context['picture'],
    }
    return context
