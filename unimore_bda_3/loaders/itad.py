from unimore_bda_3.prelude import *
import re
import json


PRICE_REGEX = re.compile(r"""Charts[.]Builder[(]setup, (.+?)[)]""")
"""
A regex to extract price JSON data from a price graph ``<script>`` object.
"""


def _load_price_series(src: dict) -> pd.Series:
    """
    Load the contents of a IsThereAnyDeal price graph series into a `pandas.Series`.
    """

    index = [pd.Timestamp(item[0], unit="ms", tz="utc") for item in src["data"]]
    data = [item[1] for item in src["data"]]

    series = pd.Series(
        data=data,
        index=index,
        name=f"""ITAD · {src["name"]}"""
    )
    if "Worst" in series.name or "High" in series.name:
        series = series.groupby(series.index.date).max()
    else:
        series = series.groupby(series.index.date).min()

    return series


def _load_price_dataframe(match: str) -> pd.DataFrame:
    """
    Load the contents of a IsThereAnyDeal price graph ``Charts.Builder`` into a `pandas.DataFrame`.
    """

    srcs: list = json.loads(match)

    dataframe = pd.DataFrame(
        data=[_load_price_series(src) for src in srcs]
    ).T
    dataframe.index = pd.to_datetime(dataframe.index)

    return dataframe


def load(fd: t.IO[str]) -> list[pd.DataFrame]:
    """
    Load the contents of a IsThereAnyDeal price graph ``<script>`` object into a `list` of `pandas.DataFrame`\\ s.
    """

    data = fd.read()
    matches: list[str] = PRICE_REGEX.findall(data)

    return [_load_price_dataframe(match) for match in matches]


__all__ = (
    "load",
)
