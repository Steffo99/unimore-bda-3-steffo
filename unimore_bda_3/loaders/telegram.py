from unimore_bda_3.prelude import *
import json


def anonymize(fd: t.IO[str]) -> t.Iterable[str]:
    """
    Read a Telegram GDPR export file, stripping everything but the messages' dates from it, returning an iterable of :class:`str`s.

    :param fd: The input file descriptor.
    :returns: An iterable of :class:`str`s.
    """
    data = json.load(fd)
    msgs = data["messages"]

    return map(lambda msg: msg["date"], msgs)


def store(data: t.Iterable[str], fd: t.IO[str]) -> None:
    """
    Write the data returned :func:`.anonymize` into the given file descriptor, as a JSON list.

    :param data: The :class:`list` to store.
    :param fd: The file descriptor to write to.
    """
    json.dump(list(data), fd)


def load(fd: t.IO[bytes]) -> pd.DataFrame:
    """
    Import a :class:`list` stored by :func:`store_telegramanon` into a :class:`pandas.DataFrame`.

    :param fd: The file descriptor to read from.
    :return: The imported :class:`pandas.DataFrame`.
    """
    data = json.load(fd)
    dataframe = pd.DataFrame(data)
    dataframe["date"] = pd.to_datetime(dataframe[0])
    del dataframe[0]
    dataframe = dataframe.set_index("date")
    return dataframe


__all__ = (
    "anonymize",
    "store",
    "load",
)
