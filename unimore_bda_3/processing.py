from unimore_bda_3.prelude import *
import unimore_bda_3.loaders as loaders


def process_game(name: str, path: Path) -> pd.DataFrame:
    steam_appid_path = path.joinpath("steam_appid.txt")
    gtrends_worldwide_path = path.joinpath("gtrends-worldwide.csv")
    steamdb_players_path = path.joinpath("steamdb-players.csv")
    steamdb_price_path = path.joinpath("steamdb-price.csv")
    itad_price_path = path.joinpath("itad-price.js")

    with open(steam_appid_path) as fd:
        steam_news: pd.DataFrame = loaders.steam.load(fd=fd)

    with open(gtrends_worldwide_path) as fd:
        google_trends: pd.DataFrame = loaders.gtrends.load(fd=fd, query_name=name)

    with open(steamdb_players_path) as fd:
        steamdb_players: pd.DataFrame = loaders.steamdb.load_players(fd=fd)

    with open(steamdb_price_path) as fd:
        steamdb_price: pd.DataFrame = loaders.steamdb.load_price(fd=fd)

    with open(itad_price_path) as fd:
        itad_prices: list[pd.DataFrame] = loaders.itad.load(fd=fd)

    dataframe: pd.DataFrame = utils.join_frames(steamdb_players, steamdb_price, google_trends, steam_news, *itad_prices)

    dataframe["SteamDB · Steam"].fillna(method="ffill", inplace=True)
    dataframe["Google Trends · Score"].fillna(method="ffill", inplace=True)
    dataframe["ITAD · Best Price"].fillna(method="ffill", inplace=True)
    dataframe["ITAD · Best Regular Price"].fillna(method="ffill", inplace=True)
    dataframe["ITAD · Worst Regular Price"].fillna(method="ffill", inplace=True)
    dataframe["ITAD · Historical Low"].fillna(method="ffill", inplace=True)
    news_columns = list(filter(lambda c: c.startswith("Steam · Count of News tagged"), dataframe.columns))
    for news_col_name in news_columns:
        dataframe[news_col_name].fillna(0, inplace=True)

    dataframe["Steam · Is there News?"] = pd.Series(data=False, dtype=bool)
    dataframe["Steam · Is there News?"] = (dataframe[news_columns] > 0).any(axis="columns")

    dataframe["SteamDB · Relative concurrent players"] = dataframe["SteamDB · Peak concurrent players"] / dataframe["SteamDB · Peak concurrent players"].max()
    dataframe["SteamDB · Relative Steam price"] = dataframe["SteamDB · Steam"] / dataframe["SteamDB · Steam"].max()
    dataframe["ITAD · Relative Best Price"] = dataframe["ITAD · Best Price"] / dataframe["ITAD · Best Price"].max()

    dataframe["ITAD · Best price change from previous day"] = dataframe["ITAD · Best Price"].diff()
    dataframe["SteamDB · Steam price change from previous day"] = - dataframe["SteamDB · Steam"].diff()

    dataframe["SteamDB · Is there a discount?"] = dataframe["SteamDB · Steam price change from previous day"] < 0
    dataframe["ITAD · Is there a discount?"] = dataframe["ITAD · Best price change from previous day"] < 0

    dataframe["Cumulative · Is something happening on Steam?"] = dataframe["Steam · Is there News?"] + dataframe["SteamDB · Is there a discount?"]
    dataframe["Cumulative · Is something happening?"] = dataframe["Steam · Is there News?"] + dataframe["SteamDB · Is there a discount?"] + dataframe["ITAD · Is there a discount?"]

    return dataframe


__all__ = (
    "process_game",
)
