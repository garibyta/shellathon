from collections import defaultdict


def exclude_empties(l):
    return [x for x in l if x]


def flatten_list(l):
    return [item for sub in l for item in sub]


def get_by(obj, by):
    return getattr(obj, by) if hasattr(obj, by) else obj[by]


def non_consecutive_groupby(iterable, key=None):
    grouped_data = defaultdict(list)
    for item in iterable:
        group_key = key(item)
        grouped_data[group_key].append(item)
    return grouped_data.items()
