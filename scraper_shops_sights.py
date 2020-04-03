import boto3
import json
import populartimes
from datetime import datetime
import time
import os
import pandas as pd
import settings

api_key = settings.API_KEY


s3_client = boto3.client('s3')
date = datetime.now()

city_csv = pd.read_csv("place_ids/hops_sights_ids.csv", sep=";", header=None)

# place_ids = [id.strip() for id in city_csv.readlines()]

place_ids = city_csv[0]

result = []
for place_id in place_ids:
    print("processing", place_id)
    try:
        key = api_key
        data = populartimes.get_id(key, place_id)
    except Exception as e:
        print(e)
        print("Error with key: " + place_id)
        continue
    if "current_popularity" in data:
        result.append(data)
    else:
        print("No Popularity-Data for " + data["name"])

s3_client.put_object(Body=json.dumps(result),  Bucket=settings.BUCKET,
              Key='googleplaces_shops_sights/{}/{}/{}/{}'.format(str(date.year).zfill(4), str(date.month).zfill(2), str(date.day).zfill(2), str(date.hour).zfill(2)))
