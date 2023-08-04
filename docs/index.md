<div align=center>

<img src="https://raw.githubusercontent.com/blaylockbk/pandas-rose/main/images/pandas-rose.png" title="Bing Image Creator: Cartoon chunky panda hugging rose in the wind pixel art " width=200>

</div>

This python package adds a custom Pandas accessor to generate polar wind rose plots from a Pandas dataframe.

I don't mean to compete with the wonderful [windrose](https://github.com/python-windrose/windrose) package already available, but that package has a little too much complexity for what I wanted. This package is meant to provide a minimal, simple interface to making wind rose plots. This is done by using Pandas methods `pd.cut` and `df.groupby` and using Matplotlib regular polar axes.

## Install

Install with pip. The requirements are only pandas, numpy, and matplotlib.

```bash
pip install pandas-rose
```

## Usage

[Tutorial](./tutorial.ipynb){.md-button .md-button--primary}

_TLDR:_ Pandas-rose is simple.

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

# Show a table of the binned data
df.rose.plot()
```

