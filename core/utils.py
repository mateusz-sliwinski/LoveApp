"""Utils.py files."""
# Standard Library
from random import randint

# 3rd-party
from accounts.utils import time_today
from core.models import Likes, DashboardLike, DashboardMatched

# Project
from accounts.models import CustomUser
from accounts.models import PhotoUser
from accounts.models import Preferences


def randomize(all_users_count, actually_user_id):  # noqa D103

    x = CustomUser.objects.all()
    y = Likes.objects.filter(user_one=actually_user_id)
    x = x.exclude(id=actually_user_id)
    for z in range(y.count()):
        x = x.exclude(id=y[z].user_two.id)

    return x[randint(0, len(x) - 1)].id


def person_and_tags(all_photo, context, current_user_id):  # noqa D103
    random = randomize(all_photo, current_user_id)
    context = take_context(context, random)

    user = CustomUser.objects.get(id=random)
    create_dislike = DashboardLike.objects.create(
        count_like=0,
        count_dislike=1,
        create_date=str(time_today()),
        custom_user=user
    )
    create_dislike.save()

    return context


def person_and_tags_for_like(all_photo, context, current_user_id, current_user):  # noqa D103
    random = randomize(all_photo, current_user_id)
    context = take_context(context, random)

    list_likes = Likes.objects.filter(user_one=random, user_two=current_user_id)

    user = CustomUser.objects.get(id=random)
    create_like = DashboardLike.objects.create(
        count_like=1,
        count_dislike=0,
        create_date=str(time_today()),
        custom_user=user
    )
    create_like.save()

    if len(list_likes) > 0:
        user_likes = Likes.objects.create(
            user_one=current_user,
            user_two=CustomUser.objects.get(id=random),
            status='Matched',
        )
        user_likes.save()

        list_likes.update(
            status='Matched',
        )

        created_matched = DashboardMatched.objects.create(
            count_matched=1,
            create_date=str(time_today()),
            custom_user=current_user,
            custom_user2=CustomUser.objects.get(id=random),
        )
        created_matched.save()

    else:
        user_likes = Likes.objects.create(
            user_one=current_user,
            user_two=CustomUser.objects.get(id=random),
            status='Liked',
        )
        user_likes.save()

    return context


def take_context(context, random):  # noqa D103
    context['picture'] = PhotoUser.objects.filter(custom_user=random).all()
    context['preferences'] = Preferences.objects.filter(custom_user=random).all()
    context = {
        'preferences': context['preferences'],
        'picture': context['picture'],
    }
    return context
