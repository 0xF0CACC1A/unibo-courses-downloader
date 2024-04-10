#!/usr/bin/env python3
import requests
import json
import sys
import re
from yt_dlp import YoutubeDL
from threading import Thread

def _download_video(url : str, name: str):
    with YoutubeDL({"quiet": True, 'outtmpl': f'{name}.mp4'}) as ydl: ydl.download(url)

def download_video(url: str, name: str):
    Thread(target=_download_video, args=[url, name]).start()
    

with open(sys.argv[1]) as f:
    cookies = json.load(f)

s = requests.Session()

# https://github.com/psf/requests/issues/3519
# https://stackoverflow.com/questions/17224054/how-to-add-a-cookie-to-the-cookiejar-in-python-requests-library
# https://www.reddit.com/r/Python/comments/6n7l79/loading_cookies_in_requests_module/
# set cookie jar
for cookie in cookies:
    # essential values
    cookie = {
        "name": cookie['name'],
        "value": cookie['value'],
        "domain": cookie['domain'],
    }
    s.cookies.set(**cookie)

folderID = sys.argv[2]
url = f'https://unibo.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID="{folderID}"&page=0&maxResults=250'
s.get(url)

with open("payload.json") as f:
    # load template for next req
    payload = json.load(f)
payload["queryParameters"]["folderID"] = folderID

url = 'https://unibo.cloud.panopto.eu/Panopto/Services/Data.svc/GetSessions'
r = s.post(url, json=payload)

regex = r'IosVideoUrl":"(https.*?mp4)"'
for (i, m) in enumerate(re.finditer(regex, r.text)):
    url = m.group(1).replace("\\", "")
    download_video(url, str(i))  
