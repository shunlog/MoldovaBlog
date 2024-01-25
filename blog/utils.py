import datetime
from math import floor

from django.utils import timezone
from django.core.exceptions import ValidationError


def file_size_validator(size):
    '''Returns a function that validates a file being smaller than size (in MiB)'''
    def check(value):
        limit = size * 1024 * 1024
        if value.size > limit:
            raise ValidationError(f'File too large. Size should not exceed {size} MiB.')
    return check


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
