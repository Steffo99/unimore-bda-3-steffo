import pandas

from unimore_bda_3.prelude import *
import cycler


def plot(name: str, *dfs: pd.DataFrame, colors: list[str]) -> tuple[plt.Figure, list[plt.Axes], list[list[mplc.BarContainer]]]:

    def split_years(df: pd.DataFrame) -> sc.SortedDict[int, pd.DataFrame]:
        groups = df.groupby(df.index.year).groups
        frames = {
            k: pd.DataFrame(index=v)
            for k, v in groups.items()
        }
        return sc.SortedDict(frames)

    dfs_by_years: list[sc.SortedDict[int, pd.DataFrame]] = [
        split_years(df)
        for df in dfs
    ]

    years: sc.SortedSet = sc.SortedSet()
    for df_by_years in dfs_by_years:
        years |= df_by_years.keys()

    def fill_years(df_by_years: dict[int, pd.DataFrame]) -> None:
        for year in years:
            df_by_years[year] = df_by_years.get(year, pd.DataFrame())

    for df_by_years in dfs_by_years:
        fill_years(df_by_years)

    def aggregate_hours(t: tuple[int, pd.DataFrame]) -> pd.DataFrame:
        n, df = t
        if len(df.index) > 0:
            df = df.groupby(by=[df.index.hour]).size().to_frame(n)
        else:
            df = pd.DataFrame(columns=[n], index=pd.Index(range(24), dtype="Int64", name="date"))

        for hour in range(24):
            df.loc[hour] = df[n].get(hour, 0)
        df = df.sort_index()
        return df

    dfs_by_years_by_hours: list[sc.SortedDict[int, list[pd.DataFrame]]] = [
        sc.SortedDict({
            year: aggregate_hours((index, df_by_year))
            for year, df_by_year in df_by_years.items()
        })
        for index, df_by_years in enumerate(dfs_by_years)
    ]

    years_zipped_dfs_by_hours: sc.SortedDict[int, list[pd.DataFrame]] = sc.SortedDict()
    for year in years:
        years_zipped_dfs_by_hours[year] = [
            df_by_years_by_hours[year]
            for df_by_years_by_hours in dfs_by_years_by_hours
        ]

    year_mdf_by_hours: sc.SortedDict[int, pd.DataFrame] = sc.SortedDict()
    for year, group in years_zipped_dfs_by_hours.items():
        year_mdf_by_hours[year] = utils.join_frames(*group).fillna(0)

    fig, axs_list = plt.subplots(nrows=len(years), tight_layout=True)
    fig: plt.Figure
    axs_list: list[plt.Axes]

    fig_default_size = fig.get_size_inches()
    fig.set_size_inches(w=fig_default_size[0], h=fig_default_size[1] * len(years))

    for index, [year, frame] in enumerate(year_mdf_by_hours.items()):
        axs = axs_list[index]
        year: int
        frame: pd.DataFrame

        axs.set_title(f'Attività oraria nelle chat "{name}" del {year}')

        axs.hist(
            x=[frame.index for _ in frame.columns],
            bins=frame.index,
            weights=frame,
            stacked=True,
            density=True,
            color=colors,
        )

        axs.xaxis.set_label("Data")
        axs.xaxis.set_major_locator(tick.MultipleLocator(base=6.0))
        axs.xaxis.set_major_formatter(tick.FuncFormatter(lambda h, p: f"{int(h)}:00"))
        axs.xaxis.set_minor_locator(tick.MultipleLocator(base=1.0))
        axs.xaxis.set_minor_formatter(tick.NullFormatter())

        axs.yaxis.set_label("Eventi")
        axs.yaxis.set_major_locator(tick.AutoLocator())
        axs.yaxis.set_minor_locator(tick.AutoMinorLocator())
        axs.yaxis.set_major_formatter(tick.PercentFormatter(xmax=1, decimals=0))
        axs.yaxis.set_minor_formatter(tick.NullFormatter())

        axs.grid(True, "major")
        axs.grid(True, "minor", dashes=(1, 4))

    return fig, axs_list


if __name__ == "__main__":
    import unimore_bda_3.loaders.telegram

    with mpl.rc_context({}):
        chats = [
            "ryg-legacy.json",
            "ryg-archive.json",
            "ryg-primary.json",
            "ryg-dnd.json",
        ]
        chats = map(lambda c: unimore_bda_3.loaders.telegram.try_load(c), chats)

        fig, axs_list = plot("RYG", *chats, colors=[
            "#816003",
            "#ff7f00",
            "#3f2580",
            "#df0000",
        ])
        fig.show()

    with mpl.rc_context({}):
        chats = [
            "unimore-studenti-archive.json",
            "unimore-extra-menouno.json",
            "unimore-studenti-chat.json",
            "unimore-studenti-offtopic.json",
            "unimore-extra-gaming.json",  # Not relevant
            "unimore-extra-politics.json",  # Not relevant
        ]
        chats = map(lambda c: unimore_bda_3.loaders.telegram.try_load(c), chats)

        fig, axs_list = plot("Unimore", *chats, colors=[
            "#a6331c",
            "#a6331c",
            "#d14224",
            "#ebbe28",
            "#5ceb28",
            "#5ceb28",
        ])
        fig.show()

    with mpl.rc_context({}):
        chats = [
            "steins-chat.json",
        ]
        chats = map(lambda c: unimore_bda_3.loaders.telegram.try_load(c), chats)

        fig, axs_list = plot("Steins", *chats, colors="lime")
        fig.show()

    with mpl.rc_context({}):
        chats = [
            "mallllco-cats.json",
        ]
        chats = map(lambda c: unimore_bda_3.loaders.telegram.try_load(c), chats)

        fig, axs_list = plot("Animaletti di Mallllco", *chats, colors="lime")
        fig.show()
