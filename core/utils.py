"""Utils.py files."""
from random import randint


def randomize(all_users_count, actually_user):

    while True:
        x = randint(1, all_users_count)
        if x != actually_user:
            break

    return x

