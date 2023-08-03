"""
Some helpful snippets for pandas-rose.
"""
import numpy as np
import matplotlib.pyplot as plt

def labels_on_top(ax):
    """Put radius labels on top of the bar plot."""
    for i in ax.get_yticks()[::2]:
        # TODO: determine if values on ax are normed
        #if table_kwargs.get("normed", None):
        #    text = f"{i:.1%}"
        #else:
        #    text = f"{i:g}"
        text = i
        ax.text(np.pi / 16, i, text, zorder=100, ha="center")
    ax.set_yticklabels([])
    return ax

def generate_polar_subplots(nrows, ncols):
    """Generate a matrix of polar subplots"""
    return plt.subplots(nrows, ncols, subplot_kw=dict(projection="polar"))

