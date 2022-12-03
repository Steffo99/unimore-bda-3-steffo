"""
This package is to be imported in all other packages with a wildcard import::

    from unimore_bda_3.prelude import *

"""

import typing as t
import matplotlib as mpl
import matplotlib.figure as mplf
import matplotlib.axes as mpla
import numpy as np
import scipy as sp
import pandas as pd
from datetime import datetime


__all__ = (
    "t",
    "mpl",
    "mplf",
    "mpla",
    "np",
    "sp",
    "pd",
    "datetime",
)
