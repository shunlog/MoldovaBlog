import datetime
from math import floor

from django.utils import timezone


def time_passed_string(t):
    """Calculate a '3 hours ago' type string from a python datetime. """
    units = {
        'years': lambda diff: diff.days / 365,
        'months': lambda diff: diff.days / 30,
        'days': lambda diff: diff.days,
        'hours': lambda diff: diff.seconds / 3600,
        'minutes': lambda diff: diff.seconds % 3600 / 60,
    }

    now = timezone.now()
    diff = now - t

    for unit in units:
        dur = floor(units[unit](diff))
        if dur < 1:
            continue
        # De-pluralize if duration is 1 ('1 day' vs '2 days')
        unit = unit[:-dur] if dur == 1 else unit
        return f'{dur} {unit} ago'
    return 'just now'
