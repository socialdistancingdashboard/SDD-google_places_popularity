import pandas as pd
import requests
import json
from tqdm import tqdm
import settings

with open("place_ids/gmap_supermarket_ids.csv") as f:
     place_ids = [key.strip() for key in f.readlines()]

data = pd.DataFrame()
for id in tqdm(place_ids):
    #print(id)
    params = {
        "key": settings.API_KEY,
        "place_id": id,
        "fields": ",".join(["place_id","address_component","name"])
    }

    r = requests.get("https://maps.googleapis.com/maps/api/place/details/json", params = params)
    data_id = pd.io.json.json_normalize(r.json()["result"])
    for component in r.json()["result"]["address_components"]:
        if 'locality' in component["types"]:
            data_id["city"] = component["long_name"]
    data = data.append(data_id)
data.to_csv("place_id_details.csv")
data.city.unique().shape
data = pd.read_csv("place_id_details.csv")
data["name"] = data["name"].str.lower()
for store in ["Edeka" , "Rewe" , "Lidl" , "Aldi"]:
    print(store)
    print(data.loc[data["name"].str.contains(store.lower())]["city"].unique().shape)
data
data = data.drop_duplicates("place_id")

result = []
for city, group in data.groupby("city"):
    group = pd.DataFrame(group)
    list = []
    for store in ["Edeka" , "Rewe" , "Lidl" , "Aldi"]:
        if any(group["name"].str.contains(store.lower())):
            list.append(group.loc[group["name"].str.contains(store.lower())]["place_id"].iloc[0])
    for x in range(4-len(list)):
        try:
            list.append(group.loc[~group["place_id"].isin(list)]["place_id"].iloc[0])
        except Exception as e:
            print(e)
            print("no more for " + city)
    if not list:
        raise Exception('{} has not enough results'.format(city))
    if city in ["Düsseldorf","Essen","Köln","Dortmund","Bonn","Duisburg","Bochum","Gelsenkirchen","Berlin","München","Stuttgart"]:
        list = group["place_id"].tolist()
    result = result + list
len(result)
pd.DataFrame(result).to_csv("place_ids/gmap_supermarket_ids.csv", index=False, header=False)
data["city"].value_counts().hist()
data.loc[data["place_id"].isin(result)]["city"].value_counts().hist()
data["city"]
