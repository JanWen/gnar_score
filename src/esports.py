import json
import os
import requests
import gzip
import shutil
from io import BytesIO


S3_BUCKET_URL = "https://power-rankings-dataset-gprhack.s3.us-west-2.amazonaws.com"

def load_team_ids():
    with open("esports-data/teams.json", "r") as json_file:
        teams_data = json.load(json_file)
    return teams_data

def get_tournaments_data():
    tournaments_json = json.load(open("esports-data/tournaments.json", "r"))
    return sorted(tournaments_json, key=lambda item: item["startDate"])


def get_s3_file(file_name):
   response = requests.get(f"{S3_BUCKET_URL}/{file_name}.json.gz")
   print(response)
   if response.status_code == 200:
       try:
           gzip_bytes = BytesIO(response.content)
           return gzip.GzipFile(fileobj=gzip_bytes, mode="rb")
           
       except Exception as e:
           print("Error:", e)
   else:
       print(response)
       print(f"Failed to download {file_name}")

def get_tournaments_s3():
    return json.load(get_s3_file("esports-data/tournaments"))
teams_data = load_team_ids()
tournaments_data = get_tournaments_data()


