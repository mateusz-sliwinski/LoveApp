"""Utils.py files."""
# Standard Library
from random import randint

# 3rd-party
from core.models import Likes

# Project
from accounts.models import CustomUser
from accounts.models import PhotoUser
from accounts.models import Preferences


def randomize(all_users_count, actually_user):  # noqa D103
    while True:
        x = randint(1, all_users_count)
        if x != actually_user:
            break

    return x


def person_and_tags(all_photo, context, current_user_id):  # noqa D103
    random = randomize(all_photo, current_user_id)
    context = take_context(context, random)
    return context


def person_and_tags_for_like(all_photo, context, current_user_id, current_user):  # noqa D103
    random = randomize(all_photo, current_user_id)
    context = take_context(context, random)

    user_likes = Likes.objects.create(
        user_one=current_user,
        user_two=CustomUser.objects.get(id=random),
        status='NUll',
    )
    user_likes.save()

    x = Likes.objects.values_list('user_one_id')
    y = Likes.objects.values_list('user_two_id')

    z = returnMatches(x, y)

    print(z.pop(random))

    if z.pop(random) == current_user_id:
        print('inside')
        Likes.objects.update(
            # id=Likes.objects.all().count(),
            status='match'
        )

    return context


def take_context(context, random):  # noqa D103
    context['picture'] = PhotoUser.objects.filter(custom_user=random).all()
    context['preferences'] = Preferences.objects.filter(custom_user=random).all()
    context = {
        'preferences': context['preferences'],
        'picture': context['picture'],
    }
    return context


def returnMatches(a, b):
    return list(set(a) & set(b))
