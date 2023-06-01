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
    labs, theme, theme_minimal, theme_matplotlib,
    expand_limits,
    theme,
    element_text,
    scale_x_datetime
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
#mkdir("00_data_wrangled")
bike_orderlines_wrangle_df.to_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl")

df = pd.read_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl")

# 6.1 Total Sales by Month ----

df['order_date'].dt.year

sales_by_month_df = df[['order_date', 'total_price']] \
    .set_index('order_date') \
    .resample(rule='MS') \
    .aggregate(np.sum) \
    .reset_index()

# Quick Plot ----
sales_by_month_df.plot(x='order_date', y='total_price')
plt.show()

# Report Plot ----
# %%
usd = currency_format(prefix="$", digits=0, big_mark=",")

ggplot(aes(x='order_date', y='total_price'), data=sales_by_month_df) + \
    geom_line() + \
    geom_smooth(method='lowess', se=False, color='blue', span =0.18 ) + \
    scale_y_continuous(labels=usd) + \
    labs(title = 'Revenue by Month',
         x ="",
         y="Revenue") + \
    theme_minimal() + \
    expand_limits(y=0)

# 6.2 Sales by Year and Category 2 ----

# ** Step 1 - Manipulate ----
df = pd.DataFrame(df)

sales_by_month_cat_2 = df[['category_2', 'order_date', 'total_price']] \
    .set_index('order_date') \
    .groupby('category_2') \
    .resample('MS') \
    .agg(np.sum) \
    .reset_index()

# Step 2 - Visualize ----
# Simple Plot
sales_by_month_cat_2 \
    .pivot(
        index='order_date',
        columns='category_2',
        values='total_price') \
    .fillna(0) \
    .plot.bar(stacked=True)
plt.show()


sales_by_month_cat_2 \
    .pivot(
        index='order_date',
        columns='category_2',
        values='total_price') \
    .fillna(0) \
    .plot(kind='line', subplots=True, layout=(3,3))
plt.show()
# Reporting Plot
ggplot(mapping=aes(x='order_date', y='total_price'),
       data=sales_by_month_cat_2) + \
        geom_line(color = "#2c3e50") + \
        geom_smooth(method="lm", se=False, color="blue") + \
        facet_wrap(facets="category_2", ncol=3, scales="free_y") + \
        theme_minimal() + \
        theme(subplots_adjust={'wspace':0.35},
              axis_text_y= element_text(size=6),
              axis_text_x= element_text(size=6)) + \
        scale_y_continuous(labels=usd) + \
        scale_x_datetime(breaks=date_breaks("2 years"),
                         labels=date_format(fmt="%Y-%m")) +\
        labs(title = "Revenue by Month",
             x="",
             y="Revenue") 


# 7.0 Writing Files ----


# Pickle ----
df.to_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl")

# CSV ----
df.to_csv("00_data_wrangled/bike_orderlines_wrangled_df.csv")

# Excel ----
df.to_excel("00_data_wrangled/bike_orderlines_wrangled_df.xlsx")

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
