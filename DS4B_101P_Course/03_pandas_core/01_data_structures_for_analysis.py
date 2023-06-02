# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 3 (Pandas Core): Data Structures ----

# IMPORTS ----
import pandas as pd 
import numpy as np 

from my_pandas_extensions.database import collect_data

df = collect_data()

# 1.0 HOW PYTHON WORKS - OBJECTS

# Objects
type(df)

type(df).mro()

# Objects have classes
type("string").mro()

# Objects have attributes
df.shape
df.columns


# Objects have methods
df.query("model == 'Jekyll Carbon 2'")



# 2.0 KEY DATA STRUCTURES FOR ANALYSIS

# - PANDAS DATA FRAME
df


# - PANDAS SERIES
df['order_date'].dt.year



# - NUMPY ARRAY
df['order_date'].values


df['price'].values.dtype


# 3.0 DATA STRUCTURES - PYTHON

# Dictionaries
d = {"a":1}
type(d)
d.keys()
d.values()
d['a']

# Lists
l = [1,"A", [2, "B"]]
l[0]
l[1]
l[2][1]

list(d.values())[0]

# Tuples
t = (10,20)
t[0]

# Base Data Types
type(1.5)
type(1)
type('string')
type(True)

# Casting
model = "Jekyll Carbon 2"
price = 6070
f"The first model is: {model}"
f"The price of the first model is: {price} "

str(price) + " some text"

int("50%".replace("%", ""))

r = list(range(1, 50))

np.array(r)

pd.Series(r).to_frame()

df['order_date'].astype('str').str.replace("-",'/')
