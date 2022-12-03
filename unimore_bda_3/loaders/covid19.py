from unimore_bda_3.prelude import *


def load(fd: t.IO[str]) -> pd.DataFrame:
    """
    Import ``dpc-covid19-ita-andamento-nazionale.json`` data from the given file descriptor into a :class:`pandas.DataFrame`.

    :param fd: The file descriptor.
    :return: The :class:`pandas.DataFrame`.
    """
    dataframe = pd.read_json(fd)
    dataframe["data"] = pd.to_datetime(dataframe["data"])
    dataframe = dataframe.set_index("data")
    return dataframe


__all__ = (
    "load",
)
