from unimore_bda_3.prelude import *


def add_scores(dataframe: pd.DataFrame):
    for base in [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.08, 1.09, 1.1, 1.11, 1.12, 1.13, 1.14, 1.15]:
        score = pd.Series(dtype=float)
        prev_date = None
        for date, value in dataframe["Cumulative · Is something happening?"].items():
            if not prev_date:
                score[date] = 0
            elif value:
                score[date] = 1
            else:
                score[date] = score[prev_date] / base
            prev_date = date

        dataframe[f"Cumulative · General happening score with base {base}"] = score
        dataframe[f"Cumulative · Scaled general happening score with base {base}"] = dataframe[f"Cumulative · General happening score with base {base}"] * dataframe["Google Trends · Score"]

    return dataframe


__all__ = (
    "add_scores",
)
