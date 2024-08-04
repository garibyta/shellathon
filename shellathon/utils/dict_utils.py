import collections
from shellathon.utils.iterable_utils import get_by


def exclude_nones(d):
    return {k: v for k, v in d.items() if v is not None}


def to_dict(l, by='name'):
    keys = [iterable_utils.get_by(obj, by) for obj in l]
    dups = [key for key, val in collections.Counter(keys).items() if val != 1]
    assert not dups, f'Found duplicated keys {dups}'

    return {iterable_utils.get_by(obj, by): obj for obj in l}
