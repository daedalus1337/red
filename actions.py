import requests
import html
import sys
import const as c
import os
from rich.table import Table
from dotenv import dotenv_values
from rich.console import Console
from rich.text import Text
import json
import configurator

console = Console(highlight=False)

def load_config():
	filename = os.path.join(os.path.dirname(__file__), 'config.json')
	with open(filename) as jsonfile:
		data = json.load(jsonfile)
		global default_release
		default_release = data["defaults"]["release"]
		global default_media
		default_media = data["defaults"]["media"]
		global default_format
		default_format = data["defaults"]["format"]
		global toplist_limit
		toplist_limit = data["toplist_limit"]
		global freeleech
		freeleech = data["freeleech"]
		global file_dir
		file_dir = data["file_dir"]

def register_key():
	api_key = input("Please enter your API key (or press Ctrl + C to exit): ")
	f = open(".env", "w")
	f.write(f"KEY='{api_key}'")
	f.close()

def make_request(params):
	header = {"Authorization": dotenv_values(".env")["KEY"]}
	req = requests.get(c.url, params=params, headers=header)
	if req.status_code != 200:
		console.print(f"Status of request is {req.status_code}. Aborting...")
		console.print(req._content)
		sys.exit()
	return req

def sizeof_fmt(num, suffix="B"):
	for unit in ["","K","M","G","T","P","E","Z"]:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, "Yi", suffix)

def print_album_info(release):
	console.print("Torrent ID: " + str(release["torrentId"]) if "torrentId" in release else "Torrent ID: " + str(release["id"]))
	console.print("Media: " + release["media"])
	console.print("Format: " + release["format"])
	console.print("Encoding: " + release["encoding"])
	console.print("Size: " + str(sizeof_fmt(release["size"])))
	if "fileCount" in release:
		console.print("Files: " + str(release["fileCount"]))
	console.print("Seeders: " + str(release["seeders"]))
	console.print("")

def search(artist, releases, media, format, album=None):
	if album:
		artist_action = {"action": "artist", "artistname": artist}
		r1 = make_request(artist_action).json()["response"]
		for group in r1["torrentgroup"]:
			if html.unescape(group["groupName"].lower()) == album.lower():
				group_action = {"action": "torrentgroup", "id": str(group["groupId"])}
				r2 = make_request(group_action).json()["response"]
				for release in r2["torrents"]:
					if release["format"] in format and release["media"] in media:
						print_album_info(release)
	else:
		action = {"action": "artist", "artistname": artist}
		r1 = make_request(action).json()["response"]
		for release in releases:
			for group in r1["torrentgroup"]:
				if c.releases[group["releaseType"]] == release:
					console.print("Release name: " + html.unescape(group["groupName"]))
					console.print("Release type: " + c.releases[group["releaseType"]])
					console.print("")

def stats():
	stats_action = {"action": "index"}
	r1 = make_request(stats_action).json()["response"]
	t = Table(title=Text(r1["username"], style="bold green"), show_header = False)
	t.add_row("Class", r1["userstats"]["class"])
	t.add_row("Ratio", str(r1["userstats"]["ratio"]))
	t.add_row("Required Ratio", str(r1["userstats"]["requiredratio"]))
	t.add_row("Upload", str(sizeof_fmt(r1["userstats"]["uploaded"])))
	t.add_row("Download", str(sizeof_fmt(r1["userstats"]["downloaded"])))
	t.add_row("Messages", Text(str(r1["notifications"]["messages"]),style="green") if r1["notifications"]["messages"] != 0 else str(r1["notifications"]["messages"]))
	console.print(t)

def inbox():
	inbox_action = {"action": "inbox"}
	r1 = make_request(inbox_action).json()["response"]
	t = Table("Sender", "Subject", "Message ID", title="Inbox")
	for item in r1["messages"]:
		if item["senderId"] == 0:
			sender = "SYSTEM"
		else:
			sender = html.unescape(item["username"])
		subject = html.unescape(item["subject"])
		messageId = str(item["convId"])
		if item["unread"] == True:
			sender = Text(sender, style="green")
			subject = Text(subject, style="green")
			messageId = Text(str(item["convId"]), style="green")
		t.add_row(sender, subject, messageId)
	console.print(t)

def torrent_download(dir, torrentid, fl):
	torrent_action = {"action": "torrent", "id": torrentid}
	r1 = make_request(torrent_action)
	album = html.unescape(r1.json()["response"]["group"]["name"])
	artist = html.unescape(str((r1.json()["response"]["group"]["musicInfo"]["artists"][0]["name"])))
	download_action = {"action": "download", "id": torrentid, "usetoken": int(fl)} if fl == True else {"action": "download", "id": torrentid}
	r2 = make_request(download_action)
	path = dir + html.unescape(artist) + " - " + html.unescape(album.replace("/","_")) + ".torrent"
	open(path, "wb").write(r2.content)
	console.print(f"Torrent for {artist} - {album} was successfully downloaded!")

def top(list, toplist_limit):
	list_action = {"action": "top10", "limit": toplist_limit}
	r1 = make_request(list_action).json()["response"]
	for item in r1:
		if item["caption"] == c.top_lists[list]:
			console.print("---")
			console.print(item["caption"])
			console.print("---")
			n = 1
			for r in item["results"]:
				if r["artist"] == False:
					console.print(str(n) + ") " + html.unescape(r["groupName"]))
				else:
					console.print(str(n) + ") " + html.unescape(str(r["artist"])) + " - " + html.unescape(str(r["groupName"])))
				print_album_info(r)
				n += 1

def read(message_id):
	read_action = {"action": "inbox", "type": "viewconv", "id": message_id}
	r1 = make_request(read_action).json()["response"]
	console.print("")
	console.print(r1["subject"])
	console.print("---")
	t = Table("Sender", "Message", show_lines = True)
	for item in r1["messages"]:
		t.add_row(item["senderName"], html.unescape(item["bbBody"]))
	console.print(t)