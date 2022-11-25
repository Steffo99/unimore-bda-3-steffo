import pandas as pd


def merge_dicts(*dicts: dict) -> dict:
    """
    Merge all :class:`dict`s passed as arguments into a single one.

    :param dicts: The :class:`dict`s to merge.
    :return: The merged :class:`dict`s.
    """
    result = dict()
    for d in dicts:
        result |= d
    return result


def join_frames(*dfs: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Join multiple :class:`pandas.DataFrame`s in a single expression.

    :param dfs: The :class:`pandas.DataFrame`s to join.
    :param kwargs: Keyword arguments to pass to :meth:`pandas.DataFrame.join`.
    :return: The resulting :class:`pandas.DataFrame`.
    """
    if len(dfs) == 0:
        return pd.DataFrame()
    elif len(dfs) == 1:
        return dfs[0]
    else:
        return dfs[0].join(dfs[1:], **kwargs)


__all__ = (
    "merge_dicts",
)
