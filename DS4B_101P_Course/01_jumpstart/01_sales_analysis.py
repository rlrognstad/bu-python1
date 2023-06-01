# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# JUMPSTART (Module 1): First Sales Analysis with Python ----

# Important VSCode Set Up:
#   1. Select a Python Interpreter: ds4b_101p
#   2. Delete terminals to start a fresh Python Terminal session

# 1.0 Load Libraries ----

# # Load Libraries
# %%

# Core Python Data Analysis
import pandas as pd
import numpy as np
# Plotting
import matplotlib.pyplot as plt
from plotnine import (
    ggplot, 
    aes, 
    geom_col,
    geom_line,
    geom_smooth,
    facet_wrap,
    scale_y_continuous, scale_x_continuous,
    labs, theme, theme_minimal, theme_matplotlib
)

from mizani.breaks import date_breaks
from mizani.formatters import date_format, currency_format

# Misc
from os import mkdir, getcwd
from rich import pretty
pretty.install()



# 2.0 Importing Data Files ----
# %%
# help(pd.read_excel)
# - Use "q" to quit
#getcwd()

bikes_df = pd.read_excel("00_data_raw/bikes.xlsx")
bikes_df

bikeshops_df = pd.read_excel("00_data_raw/bikeshops.xlsx")

orderlines_df = pd.read_excel(
    io="00_data_raw/orderlines.xlsx",
    converters={'order.date': str})
orderlines_df.info()

# %%


# 3.0 Examining Data ----

# %%
bikes_df.head()
orderlines_df

# %%
freq_count_series = bikes_df['description'].value_counts()
freq_count_series.nlargest(5)

top5_bikes_series = bikes_df['description'].value_counts().nlargest(5)

fig = top5_bikes_series.plot(kind = "barh")
fig.invert_yaxis()
plt.show()

# %%


# 4.0 Joining Data ----
bike_orderlines_joined_df = orderlines_df \
    .drop(columns='Unnamed: 0', axis=1) \
    .merge(
        right = bikes_df,
        how = 'left',
        left_on='product.id',
        right_on='bike.id'
    ) \
    .merge(
        right=bikeshops_df,
        how='left',
        left_on='customer.id',
        right_on='bikeshop.id'
    )


# 5.0 Wrangling Data ----

# * No copy
df = bike_orderlines_joined_df

# * Copy
df2 = bike_orderlines_joined_df.copy()

# * Handle Dates
df['order.date'] = pd.to_datetime(df['order.date'])

# * Show Effect: Copy vs No Copy
bike_orderlines_joined_df.info()

# * Text Columns
df.T

# * Splitting Description into category_1, category_2, and frame_material
temp_df = df['description'].str.split(pat=' - ', expand=True)

df['category.1'] = temp_df[0]
df['category.2'] = temp_df[1]
df['frame.material'] = temp_df[2]


# * Splitting Location into City and State
temp_df = df['location'].str.split(pat=', ', expand=True)
df['city'] = temp_df[0]
df['state'] = temp_df[1]
# * Price Extended
df['total.price'] = df['quantity'] * df['price']

df.sort_values('total.price', ascending=False)

# * Reorganizing
df.columns
cols_to_keep_list = [
    'order.id', 
'order.line', 
'order.date', 
#  'customer.id', 
#  'product.id',
# 'bike.id', 
'model', 
# 'description',
'quantity',  
'price', 
'total.price', 
# 'bikeshop.id',
'bikeshop.name', 
# 'location', 
'category.1', 
'category.2',
'frame.material', 
'city', 
'state']

df = df[cols_to_keep_list]

# * Renaming columns
df.columns = df.columns.str.replace(pat=".", repl="_")

bike_orderlines_wrangle_df = df

# %%
# 6.0 Visualizing a Time Series ----


# 6.1 Total Sales by Month ----


# Quick Plot ----


# Report Plot ----



# 6.2 Sales by Year and Category 2 ----

# ** Step 1 - Manipulate ----


# Step 2 - Visualize ----


# Simple Plot


# Reporting Plot



# 7.0 Writing Files ----


# Pickle ----


# CSV ----


# Excel ----


# WHERE WE'RE GOING
# - Building a forecast system
# - Create a database to host our raw data
# - Develop Modular Functions to:
#   - Collect data
#   - Summarize data and prepare for forecast
#   - Run Automatic Forecasting for One or More Time Series
#   - Store Forecast in Database
#   - Retrieve Forecasts and Report using Templates


# %%
