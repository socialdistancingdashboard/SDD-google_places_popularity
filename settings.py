import os

###API_KEY
if "gmap_key" in os.environ:
    API_KEY = os.environ["gmap_key"]
else:
    with open("api_keys.txt") as f:
            API_KEY = f.readline()

####BUCKT
if "bucket" in os.environ:
    BUCKET = os.environ["bucket"]
else:
    BUCKET = "sdd-s3-basebucket"
