import requests
import html
import os
import sys
from dotenv import load_dotenv, find_dotenv
import const as c

load_dotenv(find_dotenv())
url = "https://redacted.ch/ajax.php?"
header = {"Authorization": os.getenv("KEY")}

def make_request(params):
	req = requests.get(url, params=params, headers=header)
	if req.status_code != 200:
		print(f"Status of request is {req.status_code}. Aborting...")
		sys.exit()
	return req

def sizeof_fmt(num, suffix="B"):
	for unit in ["","K","M","G","T","P","E","Z"]:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, "Yi", suffix)

def artist_search(artist):
	""" requires 2 arguments """
	artist = {"action": "artist", "artistname": artist}
	r1 = make_request(artist).json()["response"]

	print("")
	for group in r1["torrentgroup"]:
		print("Album name: " + html.unescape(group["groupName"]))
		print("Release type: " + c.releases[group["releaseType"]])
		print("")

def album_search(artist, album, media, format):
	artist = {"action": "artist", "artistname": artist}
	r1 = make_request(artist).json()["response"]
	for group in r1["torrentgroup"]:
		if html.unescape(group["groupName"].lower()) == album:
			album = {"action": "torrentgroup", "id": str(group["groupId"])}
			r2 = make_request(album).json()["response"]
			for release in r2["torrents"]:
				if release["format"].lower() in format and release["media"].lower() in media:
					if release["encoding"] == "24bit Lossless":
						print("***THIS IS A 24-BIT RELEASE***")
					print("Torrent ID: " + str(release["id"]))
					print("Media: " + release["media"])
					print("Size: " + str(sizeof_fmt(release["size"])))
					print("Files: " + str(release["fileCount"]))
					print("Seeders: " + str(release["seeders"]))
					print("")

def torrent_download(tid, fl):
	details_params = {"action": "torrent", "id": tid}
	r1 = make_request(details_params)
	album = r1.json()["response"]["group"]["name"]
	artist = str((r1.json()["response"]["group"]["musicInfo"]["artists"][0]["name"]))
	download_params = {"action": "download", "id": tid, "usetoken": fl}
	r2 = make_request(download_params)
	path = os.getenv("FILE_DIR") + artist + " - " + album + ".torrent"
	open(path, "wb").write(r2.content)
	print(f"Torrent for {artist} - {album} was successfully downloaded!")

def user_stats():
    stats = {"action": "index"}
    r1 = requests.get(url, params=stats, headers=header).json()["response"]
    print("Username........." + r1["username"])
    print("Class............" + r1["userstats"]["class"])
    print("Ratio............" + str(r1["userstats"]["ratio"]))
    print("Required Ratio..." + str(r1["userstats"]["requiredratio"]))
    print("Upload..........." + str(sizeof_fmt(r1["userstats"]["uploaded"])))
    print("Download........." + str(sizeof_fmt(r1["userstats"]["downloaded"])))
    print("Messages........." + str(r1["notifications"]["messages"]))
