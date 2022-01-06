#!/usr/bin/env python
import pandas as pd
import numpy as np
import seaborn as sns
import sys

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure

matplotlib.rcParams['figure.figsize'] = (12,8)

pd.options.mode.chained_assignment = None

# read the data file
df = pd.read_csv(sys.argv[1])

# Remove rows with empty values / NaN
df_less_missing_values = df.dropna(axis=0, how ='any')

# Remove rows with negative values in "Qunt" column
df_less_negative_values = df_less_missing_values[df_less_missing_values['Qunt'] >0]

# Remove outliers in "Qunt" column
# First I checked for std with df_less_negative_values["Qunt"].describe()

df_less_qunt_outliers = df_less_negative_values[df_less_negative_values["Qunt"] < 200]

# Remove outliers in "Total(Ton)" column
# First I checked for std with df_less_negative_values["Total(Ton)"].describe()
df_less_qunt_outliers[df_less_qunt_outliers['Total(Ton)'] < 50]

df.to_csv('output.csv')
