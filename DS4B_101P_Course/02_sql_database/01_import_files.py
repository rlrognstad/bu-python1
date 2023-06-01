# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 2 (Pandas Import): Importing Files ----

# IMPORTS ----
import pandas as pd

# 1.0 FILES ----

# - Pickle ----
pd.read_pickle("./00_data_wrangled/bike_orderlines_wrangled_df.pkl")

# - CSV ----
pd.read_csv("./00_data_wrangled/bike_orderlines_wrangled_df.csv", parse_dates=['order_date']).info()

# - Excel ----
pd.read_excel("./00_data_wrangled/bike_orderlines_wrangled_df.xlsx")
