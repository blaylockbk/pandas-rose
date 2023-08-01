import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import inspect
import itertools


@pd.api.extensions.register_dataframe_accessor("rose")
class RoseAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def table(
        self,
        dir_column="wind_direction",
        var_column="wind_speed",
        *,
        sectors=16,
        bins=None,
        normed=False,
    ):
        """Generate a table of the variable binned by wind direction

        Parameters
        ----------
        dir_column, var_columns: str
            The name of the column representing the wind direction and
            the variable (i.e., wind speed)
        sectors : int
            The number of direction bins
        bins : array
            The bin interval for the variable data
        normed : bool
            If False, return bin as counts.
            If True, return bin as percentage (counts divided by total count).
        """

        # Prepare the dataframe
        # Only consider the columns used for var and direction and drop
        # any rows that have a nan value.
        df = self._obj
        df = df[[var_column, dir_column]]
        df = df.dropna()

        # Direction bins (i.e., wind direction bins)
        # Sectors are centered on the bin they represent. For example,
        # for 8 sectors I need to get angles [-22.5,22.5) binned in the
        # "North" bin, not [0,45).
        width = 360 / sectors
        dir_bins = np.arange(-width / 2, 360, width)
        df.loc[df[dir_column] > 360 - (width / 2), dir_column] -= 360

        # Variable bins (i.e., wind speed bins)
        if bins is None:
            bins = np.linspace(df[var_column].min(), df[var_column].max(), 6).round(1)

        var_bins = pd.IntervalIndex.from_breaks(
            list(bins) + [float("inf")], closed="left"
        )

        # Create the bins
        df["dir_bin"] = pd.cut(df[dir_column], dir_bins)
        df["var_bin"] = pd.cut(df[var_column], var_bins)

        # Group the data by wind direction and wind speed bins
        grouped = df.groupby(["dir_bin", "var_bin"])
        table = grouped.size().unstack()

        if normed:
            table = table / len(df)

        return table

    def bar(self, **kwargs):
        """Plot the binned data as a simple bar plot"""
        table = self._obj.rose.table(**kwargs)
        ax = table.plot(kind="bar", stacked=True, figsize=(12, 6), zorder=100)

        # Set labels and title
        plt.xlabel("Wind Direction bins (degrees)")
        plt.ylabel("Frequency")

        ax.grid(ls="--", alpha=0.5)

        return ax

    def plot(self, spacing=3, figsize=(7, 6), colors="viridis", **kwargs):
        """Plot the binned data as a windrose

        Parameters
        ----------
        dir_column, var_columns: str
            The name of the column representing the wind direction and
            the variable (i.e., wind speed)
        sectors : int
            The number of direction bins
        bins : array
            The bin interval for the variable data
        normed : bool
            If False, return bin as counts.
            If True, return bin as percentage (counts divided by total count).
        spacing : number
            The spacing between sections, in degrees.
        figsize : tuple
            Size of the figure (width, height)
        colors : str or list
            Name of a matplotlib colormap, or a list of colors.
        **kwargs
            kwargs for bar plot.

            Note: the kwargs for self.table are popped from this
            functions kwargs.
        """

        # Split kwargs into kwargs for table and kwargs for plot.
        table_parms = list(inspect.signature(self.table).parameters)
        kwarg_list = list(kwargs)
        table_kwargs = {d: kwargs.pop(d) for d in kwarg_list if d in table_parms}

        table = self._obj.rose.table(**table_kwargs)
        nsectors, nbins = table.shape
        radian_locs = np.arange(0, np.pi * 2, np.pi * 2 / len(table))

        fig = plt.figure(figsize=figsize)
        ax = plt.subplot(projection="polar")
        ax.set_theta_zero_location("N")  # theta=0 at the top
        ax.set_theta_direction(-1)  # theta increasing clockwise

        kwargs.setdefault("edgecolor", "k")
        kwargs.setdefault("linewidth", 0.5)
        kwargs.setdefault("zorder", 1)
        kwargs.setdefault("alpha", 1)

        if isinstance(colors, str):
            colors = [plt.get_cmap(colors)(i) for i in np.linspace(0, 1, nbins)]
        else:
            colors = itertools.cycle(colors)

        for i, color in zip(range(nbins), colors):
            ax.bar(
                radian_locs,
                table.T.iloc[i],
                width=np.deg2rad(360 / nsectors) - np.deg2rad(spacing),
                bottom=table.T.iloc[0:i].sum(),
                color=color,
                label=table.T.iloc[i].name,
                **kwargs,
            )

        # -----------
        # Cosmetics

        # maximum radius
        ax.set_rmax(np.max(ax.get_yticks()))

        ax.set_xticks(
            np.arange(0, 2 * np.pi, np.pi / 4),
            ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
        )

        # Matplotlib doesn't let you put the bar above the grid but
        # below the axis tick labels. So, we will add the tick "y"
        # ticks and labels manually, on top of the bar.
        # TODO: Now, this makes is hard for the user to customize what
        # TODO:   they want the ticks to look like (they can't use the
        # TODO:   set_ytick* methods anymore). Maybe make this optional
        # TODO:   or tell a user how to do this.
        # TODO: PERHAPS MOVE THIS OUT AS AN OPTIONAL FUNCTION OR SNIPPET
        for i in ax.get_yticks()[::2]:
            if table_kwargs.get("normed", None):
                text = f"{i:.1%}"
            else:
                text = f"{i:g}"
            ax.text(np.pi / 16, i, text, zorder=100, ha="center")
        ax.set_yticklabels([])

        ax.grid(axis="x")
        ax.grid(axis="y", alpha=0.5)

        ax.legend(fontsize=10, bbox_to_anchor=(1.4, 0.9))

        return ax
