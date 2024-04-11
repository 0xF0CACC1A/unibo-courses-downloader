#!/usr/bin/env python3
import requests
import json
import sys
import re
from yt_dlp import YoutubeDL
from threading import Thread

def download_video(url : str, out: str):
    with YoutubeDL({"quiet": True, 'outtmpl': f'{out}'}) as ydl: ydl.download(url)

with open(sys.argv[1]) as f:
    cookies = json.load(f)

s = requests.Session()

# https://stackoverflow.com/questions/17224054/how-to-add-a-cookie-to-the-cookiejar-in-python-requests-library
# https://www.reddit.com/r/Python/comments/6n7l79/loading_cookies_in_requests_module/
# set cookie jar with essential std values
for cookie in cookies:
    cookie = {
        "name": cookie['name'],
        "value": cookie['value'],
        "domain": cookie['domain'],
    }
    s.cookies.set(**cookie)

folderID = sys.argv[2]
url = f'https://unibo.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID="{folderID}"&page=0&maxResults=250'
s.get(url)

# load payload template for next req
with open("payload.json") as f:
    payload = json.load(f)
payload["queryParameters"]["folderID"] = folderID

url = 'https://unibo.cloud.panopto.eu/Panopto/Services/Data.svc/GetSessions'
r = s.post(url, json=payload)

regex = r'"FolderName":"(.*?)".*?"IosVideoUrl":"(https.*?mp4)"'
for (i, m) in enumerate(re.finditer(regex, r.text)):
    folderName = m.group(1).replace("\\/", " ")
    url = m.group(2).replace("\\", "")
    Thread(target=download_video, args=[url, f"{folderName}/{str(i)}.mp4"]).start()
