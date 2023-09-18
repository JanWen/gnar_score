import json
import os
import requests
import gzip
import shutil
from io import BytesIO


S3_BUCKET_URL = "https://power-rankings-dataset-gprhack.s3.us-west-2.amazonaws.com"

def tournaments():
    tournaments_data = json.load(open("esports-data/tournaments.json", "r"))

    print("Tournaments:" + str(len(tournaments_data)))

    stages = 0
    matches = 0

    for tournament in tournaments_data:
        print(tournament["name"])
        stages += len(tournament["stages"])
        for stage in tournament["stages"]:
            for section in stage["sections"]:
                matches += len(section["matches"])

    print("Stages:" + str(stages))
    print("Matches:" + str(matches))

def elo_form(x,y):
    ea = 1/(1+10**((y-x)/400))
    eb = 1/(1+10**((x-y)/400))

    ra = x + 32*(1-ea)
    return ra

def get_stages():

    tournaments_data = json.load(open("esports-data/tournaments.json", "r"))

    print("Tournaments:" + str(len(tournaments_data)))

    stages = 0
    matches = 0
    stages = []
    for tournament in tournaments_data:
        for stage in tournament["stages"]:
            stages.append(stage["name"])
    for i in set(stages):
        print(i)

ESPORTSTMNT05:1831534

def download_gzip_and_write_to_json(file_name):
   # If file already exists locally do not re-download game
#    if os.path.isfile(f"{file_name}.json"):
#        return

   response = requests.get(f"{S3_BUCKET_URL}/{file_name}.json.gz")
   print(response)
   if response.status_code == 200:
       try:
           gzip_bytes = BytesIO(response.content)
           with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
               with open(f"out.json", 'wb') as output_file:
                   shutil.copyfileobj(gzipped_file, output_file)
               print(f"{file_name}.json written")
       except Exception as e:
           print("Error:", e)
   else:
       print(response)
       print(f"Failed to download {file_name}")

print("ij")

download_gzip_and_write_to_json("games/ESPORTSTMNT05:1831534")