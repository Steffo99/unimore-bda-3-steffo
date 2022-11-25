from unimore_bda_3.prelude import *
import httpx
import collections


steam_api = httpx.Client(base_url="https://api.steampowered.com")


def _load_news(appid: int) -> list[dict]:
    """
    Load all news items for the given app id, from the most recent to the least recent.
    """

    count = 100
    enddate = {}
    newsitems = []

    while count == 100:
        request = steam_api.get(
            "/ISteamNews/GetNewsForApp/v0002/", 
            params={
                "appid": appid,
                "count": 100,
                "format": "json",
                **enddate,
            }
        )
        request.raise_for_status()
        data = request.json()["appnews"]
        count = len(data["newsitems"])
        newsitems.extend(data["newsitems"])
        enddate = {"enddate": newsitems[-1]["date"]}

    return newsitems


def _categorize_news(news: list[dict]) -> dict[str, list[dict]]:
    """
    Group news items by their tags.
    """
    
    result = collections.defaultdict(list)

    for item in news:
        tags = item.get("tags", [])
        if tags:
            for tag in set(item.get("tags", [])):
                result[tag].append(item)
        else:
            result["no_tags"].append(item)
    
    return result


def _serialize_news(name: str, news: list[dict]) -> pd.Series:
    """
    Convert a list of news into a `pandas.Series` with the dates as index and 1 as the data.
    """
    
    index = pd.to_datetime([datetime.fromtimestamp(item["date"]) for item in news])
    
    return pd.Series(
        data=[1 for _ in index],
        index=index,
        name=f"""Steam · Count of News tagged {name}""",
        dtype=np.uint8,
    )


def fetch(appid: int) -> pd.DataFrame:
    """
    Load announcements related to a certain app id into a `pandas.DataFrame`.
    """

    raw_news = _load_news(appid=appid)
    categorized_news = _categorize_news(news=raw_news)
    serialized_news = [_serialize_news(name=name, news=news).to_frame() for name, news in categorized_news.items()]

    dataframe = utils.join_frames(*serialized_news).fillna(0)
    dataframe = dataframe.groupby(dataframe.index.date).sum()
    dataframe.index = pd.to_datetime(dataframe.index)

    return dataframe


def load(fd: t.IO[str]) -> pd.DataFrame:
    """
    Load announcements related to the app id contained in the given file into a `pandas.DataFrame`.
    """

    appid = int(fd.read().strip())
    data = fetch(appid=appid)

    return data


__all__ = (
    "fetch",
    "load",
)
