from unimore_bda_3.prelude import *


def load(fd: t.IO[str], index_name: str) -> pd.DataFrame:
    """
    Import a Google Trends CSV file into a :class:`pandas.Series`.

    :param fd: The file descriptor of the CSV file.
    :param index_name: The name of the column to be set as index.
    :return: The imported :class:`pandas.Series`.
    """
    dataframe = pd.read_csv(fd, sep=",", header=1)
    dataframe = dataframe.set_index(index_name)
    return dataframe
