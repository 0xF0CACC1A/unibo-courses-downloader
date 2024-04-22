#!/usr/bin/env python3
import json, os, re, requests, sys
from threading import Thread

def set_session_cookies(s: requests.Session, cookies: list[dict[str, str]]):
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

def download_video(url : str, out: str):
    from yt_dlp import YoutubeDL
    with YoutubeDL({"quiet": True, 'outtmpl': f'{out}'}) as ydl: ydl.download(url)

def download_recordings(cookies: list[dict[str, str]], folderID : str):
    s = requests.Session()
    set_session_cookies(s,cookies)

    url = f'https://unibo.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID="{folderID}"&page=0&maxResults=250'
    s.get(url)

    # load payload template for next req
    with open("payload.json") as f:
        payload = json.load(f)
    payload["queryParameters"]["folderID"] = folderID # TODO archived videos

    url = 'https://unibo.cloud.panopto.eu/Panopto/Services/Data.svc/GetSessions'
    r = s.post(url, json=payload)

    regex = r'"FolderName":"(.*?)".*?"IosVideoUrl":"(https.*?[mp4|m3u8])"'
    for (i, m) in enumerate(re.finditer(regex, r.text)):
        folderName = m.group(1).replace("\\/", " ")
        url = m.group(2).replace("\\", "")
        Thread(target=download_video, args=[url, f"{folderName}/{str(i)}.mp4"]).start()

def download_file(s: requests.Session, url: str, name: str):
    r = s.get(url)    
    with open(name,'wb+') as f: f.write(r.content) # + => create file
    print(f"scaricato {name}!")

def download_slides(cookies: list[dict[str, str]], id: str):
    s = requests.Session()
    set_session_cookies(s,cookies)
    
    r = s.get(f"https://virtuale.unibo.it/course/view.php?id={id}")
    regex = r'<a href="(https:\/\/virtuale\.unibo\.it\/mod\/{0}\/view.php\?id=([0-9]+))[\s\S]*?<h5 class="mb-0">([\s\S]*?)<\/h5>[\s\S]*?<\/a>'
    slides = [(m.group(1), m.group(3).strip()) for m in re.finditer(regex.format("resource"), r.text)]
    # urls = [(m.group(1), m.group(3).strip()) for m in re.finditer(regex.format("url"), r.text)]
    folders = [(f"https://virtuale.unibo.it/mod/folder/download_folder.php?id={m.group(2)}", m.group(3).strip()) for m in re.finditer(regex.format("folder"), r.text)]

    out_dir = id # TODO get course's name
    os.mkdir(out_dir) if not os.path.exists(out_dir) else exit(f"{out_dir} already existed!")
    # for url in urls:
    #     r = s.get(url[0])
    #     regex = r'<div class="urlworkaround">.*?<a href="(.*?)">.*?<\/a><\/div>'
    #     res = re.search(regex, r.text)
    #     if res == None: raise Exception(f"no match found\nurl: {url}\nregex: {regex}")
    #     Thread(target=download_file, args=[s, res.group(1), f"{out_dir}/{url[1].replace('/', '-')}.pdf"]).start()
    for f in folders:
        Thread(target=download_file, args=[s, f[0], f"{out_dir}/{f[1].replace('/', '-')}.zip"]).start()
    for f in slides:
        Thread(target=download_file, args=[s, f[0], f"{out_dir}/{f[1].replace('/', '-')}.pdf"]).start()

def main():
    with open(sys.argv[2]) as f: cookies = json.load(f)
    download_recordings(cookies, sys.argv[3]) if sys.argv[1] == "panopto" else download_slides(cookies, sys.argv[3])

if __name__ == "__main__":
    main()
