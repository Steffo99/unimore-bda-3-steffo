import matplotlib.pyplot as plt
import pandas as pd

from unimore_bda_3.prelude import *


def plot(data: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
    s_dates: pd.Series = data.index
    s_positives: pd.Series = data["totale_positivi"]

    fig, axs = plt.subplots()
    fig: plt.Figure
    axs: plt.Axes

    axs.set_title("Positivi giornalieri al virus COVID-19 in Italia")
    axs.plot(s_dates, s_positives)

    loc_month = mpld.MonthLocator(interval=3)
    loc_years = mpld.YearLocator()

    form_num = tick.ScalarFormatter(useLocale=True)
    form_num.set_scientific(False)

    axs.xaxis.set_label("Data")
    axs.xaxis.set_major_locator(loc_years)
    axs.xaxis.set_major_formatter(mpld.AutoDateFormatter(loc_years, defaultfmt="%Y"))
    axs.xaxis.set_minor_locator(loc_month)
    axs.xaxis.set_minor_formatter(tick.NullFormatter())

    axs.yaxis.set_label("Positivi")
    axs.yaxis.set_major_locator(tick.AutoLocator())
    axs.yaxis.set_minor_locator(tick.AutoMinorLocator())
    axs.yaxis.set_major_formatter(form_num)
    axs.yaxis.set_minor_formatter(tick.NullFormatter())

    axs.grid(True, "major")
    axs.grid(True, "minor", dashes=(1, 4))

    return fig, axs


if __name__ == "__main__":
    import unimore_bda_3.loaders.covid19

    with open("data/covid19/dati-json/dpc-covid19-ita-andamento-nazionale.json") as file:
        df = unimore_bda_3.loaders.covid19.load(file)

    fig, axs = plot(df)

    fig.show()
