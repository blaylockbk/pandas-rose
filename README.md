<div align=center>

<img src="https://raw.githubusercontent.com/blaylockbk/pandas-rose/main/images/pandas-rose.png" title="Bing Image Creator: Cartoon chunky panda hugging rose in the wind pixel art " width=200>

</div>

# Pandas Rose

This python package adds a custom Pandas accessor to generate polar wind rose plots from a Pandas dataframe.

I don't mean to compete with the wonderful [windrose](https://github.com/python-windrose/windrose) package already available, but that package has a little too much complexity for what I wanted. This package is meant to provide a minimal, simple interface to making wind rose plots. This is done by using Pandas methods `pd.cut` and `df.groupby` and using Matplotlib regular polar axes.

# Install

> ## TODO: Publish and Upload to PyPI

Install with pip. The requirements are only pandas, numpy, and matplotlib.

```bash
pip install pandas-rose
```

# Usage

Pandas-rose is simple.

```python
import pandas as pd
import rose

# df is a pandas dataframe with columns
# "wind_speed" and "wind_direction"
df = pd.DataFrame({
    "wind_speed":[1,2,3,4],
    "wind_direction":[20, 10, 190,300]
})

# Display a polar wind plot of the data
df.rose.plot()
```

![Alt text](https://raw.githubusercontent.com/blaylockbk/pandas-rose/main/images/sample_plot.png)

You can specify the pandas column to use for wind direction and wind speed. You may also change the number of sectors to bin the wind direction .

```python
df.rose.plot(
    var_column="A",    # name of variable column
    dir_column="B",    # name of direction column
    sectors=8,         # number of sectors (direction bins)
    bins=range(0,30,5) # specify variable bins
    normed=False       # If True, values as percentage instead of counts
    colors='Blues'     # Name of matplotlib colormap or list of colors
    )
```

There are two other accessors that give some information.

```python
# Display a dataframe of the binned values
df.rose.table(sectors=8)
```

![Alt text](https://raw.githubusercontent.com/blaylockbk/pandas-rose/main/images/sample_table.png)

```python
# Display the binned data as bar graph on regular axes.
df.rose.bar()
```

![Alt text](https://raw.githubusercontent.com/blaylockbk/pandas-rose/main/images/sample_bar.png)
