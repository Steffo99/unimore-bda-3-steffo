from unimore_bda_3.prelude import *


def load_players(fd: t.IO[str]) -> pd.DataFrame:
    """
    Import a SteamDB "Lifetime player count history" CSV file into a `pandas.DataFrame`.
    """

    dataframe = pd.read_csv(fd, sep=",")

    dataframe.rename(inplace=True, columns={
        "DateTime": "Date",
        "Players": "SteamDB · Peak concurrent players",
        "Average Players": "SteamDB · Day average of concurrent players",
        "Flags": "SteamDB · Player count flags",
    })

    dataframe["Date"] = pd.to_datetime(dataframe["Date"])

    dataframe.set_index("Date", inplace=True)

    dataframe = dataframe.groupby(dataframe.index.date).max()
    dataframe.index = pd.to_datetime(dataframe.index)

    return dataframe


def load_price(fd: t.IO[str]) -> pd.DataFrame:
    """
    Import a SteamDB "Price history" CSV file into a `pandas.DataFrame`.
    """

    dataframe = pd.read_csv(fd, sep=",")

    dataframe.rename(inplace=True, columns={
        "DateTime": "Date",
        "Final price": "SteamDB · Steam",
        "Flags": "SteamDB · Price flags",
    })

    dataframe["Date"] = pd.to_datetime(dataframe["Date"])

    dataframe.set_index("Date", inplace=True)

    dataframe = dataframe.groupby(dataframe.index.date).min()
    dataframe.index = pd.to_datetime(dataframe.index)

    return dataframe
