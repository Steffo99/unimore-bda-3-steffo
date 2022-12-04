"""
This package is to be imported in all other packages with a wildcard import::

    from unimore_bda_3.prelude import *

"""

import typing as t
import matplotlib.ticker as tick
import matplotlib.pyplot as plt
import matplotlib.dates as mpld
import matplotlib.container as mplc
import numpy as np
import scipy as sp
import pandas as pd
from datetime import datetime


__all__ = (
    "t",
    "tick",
    "plt",
    "mplc",
    "mpld",
    "np",
    "sp",
    "pd",
    "datetime",
)
