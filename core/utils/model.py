__author__ = 'andrew.shvv@gmail.com'


def calculate_len(choices):
    """
        Calculate length for choice filed in django model.
    """
    return max([len(t) for t in choices]) + 1
