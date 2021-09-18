from dotenv.main import find_dotenv
import requests
import html
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
url = "https://redacted.ch/ajax.php?"
header = {"Authorization": os.getenv("KEY")}

#incomplete.  API only provides integer, so I"m stuck having to manually add these as I identify them.
releases = {
	1: "Album",
	3: "Soundtrack",
	5: "EP",
	6: "Anthology",
	7: "Compilation",
	9: "Single",
	11: "Live Album",
	13: "Remix",
	14: "Bootleg",
	17: "Demo",
	18: "Concert Recording",
	19: "DJ Mix",
	1021: "Produced Bys",
	1022: "Composition",
	1023: "Remixed Bys",
	1024: "Guest Appearance"
}

def sizeof_fmt(num, suffix="B"):
	for unit in ["","K","M","G","T","P","E","Z"]:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, "Yi", suffix)

def artist_search(artist):
	""" requires 2 arguments """
	artist = {"action": "artist", "artistname": artist}
	r1 = requests.get(url, params=artist, headers=header)
	r1_json = r1.json()["response"]

	print("")
	for group in r1_json["torrentgroup"]:
		print("Album name: " + html.unescape(group["groupName"]))
		print("Release type: " + releases[group["releaseType"]])
		print("")

def album_search(artist, album):
	artist = {"action": "artist", "artistname": artist}
	r1 = requests.get(url, params=artist, headers=header)
	r1_json = r1.json()["response"]
	for group in r1_json["torrentgroup"]:
		if html.unescape(group["groupName"].lower()) == album:
			album = {"action": "torrentgroup", "id": str(group["groupId"])}
			r2 = requests.get(url, params=album, headers=header)
			r2_json = r2.json()["response"]
			for release in r2_json["torrents"]:
				if release["format"] == "FLAC":
					if release["media"] != "Vinyl":
						if release["encoding"] == "24bit Lossless":
							print("***THIS IS A 24-BIT RELEASE***")
						print("Torrent ID: " + str(release["id"]))
						print("Group ID: " + str(group["groupId"]))
						print("Media: " + release["media"])
						print("Size: " + str(sizeof_fmt(release["size"])))
						print("Files: " + str(release["fileCount"]))
						print("Seeders: " + str(release["seeders"]))
						print("")
		else:
			continue

def torrent_download(tid, fl):
	if fl == False:
		download_params = {"action": "download", "id": tid}
	elif fl == True:
		download_params = {"action": "download", "id": tid, "usetoken": True}
	details_params = {"action": "torrent", "id": tid}
	r1 = requests.get(url, params=details_params, headers=header)
	album = r1.json()["response"]["group"]["name"]
	artist = str((r1.json()["response"]["group"]["musicInfo"]["artists"][0]["name"]))
	r2 = requests.get(url, params=download_params, headers=header)
	open(os.getenv("FILE_DIR") + artist + " - " + album + ".torrent", "wb").write(r2.content)

def user_stats():
    stats = {"action": "index"}
    r1 = requests.get(url, params=stats, headers=header)
    r1_json = r1.json()["response"]
    print("Username........." + r1_json["username"])
    print("Class............" + r1_json["userstats"]["class"])
    print("Ratio............" + str(r1_json["userstats"]["ratio"]))
    print("Required Ratio..." + str(r1_json["userstats"]["requiredratio"]))
    print("Upload..........." + str(sizeof_fmt(r1_json["userstats"]["uploaded"])))
    print("Download........." + str(sizeof_fmt(r1_json["userstats"]["downloaded"])))
    print("Messages........." + str(r1_json["notifications"]["messages"]))