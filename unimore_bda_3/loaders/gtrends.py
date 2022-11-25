from unimore_bda_3.prelude import *


def load(fd: t.IO[str], query_name: str) -> pd.DataFrame:
    """
    Import a Google Trends CSV file into a :class:`pandas.DataFrame`.
    """

    dataframe = pd.read_csv(fd, sep=",", header=1)

    dataframe.rename(inplace=True, columns={
        "Mese": "Date",
        f"{query_name}: (Tutto il mondo)": "Google Trends · Score",
    })

    dataframe["Date"] = pd.to_datetime(dataframe["Date"])
    dataframe["Google Trends · Score"] = dataframe["Google Trends · Score"].map(lambda x: int(x) if x != "< 1" else 0) / 100

    dataframe.set_index("Date", inplace=True)

    return dataframe
