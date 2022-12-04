from unimore_bda_3.prelude import *
import functools


def plot(name: str, *dfs: pd.DataFrame) -> tuple[plt.Figure, plt.Axes, list[mplc.BarContainer]]:

    def aggregate_df(t: tuple[int, pd.DataFrame]) -> pd.DataFrame:
        n, df = t
        return df.groupby(by=pd.Grouper(freq="M")).size().to_frame(n)

    # noinspection PyTypeChecker
    monthly_counts_frames: list[pd.DataFrame] = list(map(aggregate_df, enumerate(dfs)))
    main_frame: pd.DataFrame = monthly_counts_frames[0].join(monthly_counts_frames[1:], how="outer").fillna(0)

    fig, axs = plt.subplots()
    fig: plt.Figure
    axs: plt.Axes

    axs.set_title(f'Attività mensile nelle chat "{name}"')
    _, _, bar_groups = axs.hist(
        x=[main_frame.index for _ in main_frame.columns],
        bins=main_frame.index,
        weights=main_frame,
        stacked=True
    )

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

    return fig, axs, bar_groups


if __name__ == "__main__":
    import unimore_bda_3.loaders.telegram

    chats = [
        "ryg-legacy.json",
        "ryg-archive.json",
        "ryg-primary.json",
        "ryg-dnd.json",
    ]
    chats = map(lambda c: unimore_bda_3.loaders.telegram.try_load(c), chats)

    fig, axs, bar_groups = plot("RYG", *chats)

    for bar in bar_groups[0]:
        bar.set_facecolor("#816003")
    for bar in bar_groups[1]:
        bar.set_facecolor("#ff7f00")
    for bar in bar_groups[2]:
        bar.set_facecolor("#3f2580")
    for bar in bar_groups[3]:
        bar.set_facecolor("#df0000")

    fig.show()

    chats = [
        "unimore-studenti-archive.json",
        "unimore-extra-menouno.json",
        "unimore-studenti-chat.json",
        "unimore-studenti-offtopic.json",
        "unimore-extra-gaming.json",  # Not relevant
        "unimore-extra-politics.json",  # Not relevant
    ]
    chats = map(lambda c: unimore_bda_3.loaders.telegram.try_load(c), chats)

    fig, axs, bar_groups = plot("Unimore", *chats)

    for bar in bar_groups[0]:
        bar.set_facecolor("#a6331c")
    for bar in bar_groups[1]:
        bar.set_facecolor("#a6331c")
    for bar in bar_groups[2]:
        bar.set_facecolor("#d14224")
    for bar in bar_groups[3]:
        bar.set_facecolor("#ebbe28")
    for bar in bar_groups[4]:
        bar.set_facecolor("#5ceb28")
    for bar in bar_groups[5]:
        bar.set_facecolor("#5ceb28")

    fig.show()

    chats = [
        "steins-chat.json",
    ]
    chats = map(lambda c: unimore_bda_3.loaders.telegram.try_load(c), chats)

    fig, axs, bars = plot("Steins", *chats)

    fig.show()

    chats = [
        "mallllco-cats.json",
    ]
    chats = map(lambda c: unimore_bda_3.loaders.telegram.try_load(c), chats)

    fig, axs, bars = plot("Animaletti di Mallllco", *chats)

    fig.show()
