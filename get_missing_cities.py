import requests
import pandas as pd
import datetime
import json
import numpy as np
from coords_to_kreis import coords_convert

ags = pd.read_csv("super_ags.csv")["0"]
ags

cities = pd.read_csv("de_cities.csv", sep = ",")
cities = cities.iloc[:,:3]
cities.columns = ["stadt", "lat", "lon"]
cities["ags"] = coords_convert(cities)
cities.shape
len(cities["ags"].unique())
cities = cities.drop_duplicates("ags")
cities.to_csv("de_cities_unique_ags.csv")
cities.shape
cities = cities.loc[~cities["ags"].isin(ags)]
cities
cities.iloc[:,0:3]
cities.iloc[:,:3].to_csv("missing.csv")
