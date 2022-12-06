import requests
import html
import sys
import const as c
from prettytable import PrettyTable, ALL
import os
from termcolor import colored
from rich.table import Table
from dotenv import dotenv_values
from rich.console import Console

console = Console(highlight=False)

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
		artist_action = {"action": "artist", "artistname": artist.lower()}
		r1 = make_request(artist_action).json()["response"]
		for group in r1["torrentgroup"]:
			if html.unescape(group["groupName"].lower()) == album.lower():
				group_action = {"action": "torrentgroup", "id": str(group["groupId"])}
				r2 = make_request(group_action).json()["response"]
				for release in r2["torrents"]:
					if format is None and media is None:
						print_album_info(release)
					elif media is None and format is not None:
						if release["format"].lower() in format:
							print_album_info(release)
					elif format is None and media is not None:
						if release["media"].lower() in media:
							print_album_info(release)
					elif release["format"].lower() in format and release["media"].lower() in media:
						print_album_info(release)
	else:
		action = {"action": "artist", "artistname": artist.lower()}
		r1 = make_request(action).json()["response"]
		if releases is None:
			for group in r1["torrentgroup"]:
				console.print("Release name: " + html.unescape(group["groupName"]))
				console.print("Release type: " + c.releases[group["releaseType"]])
				console.print("")
		elif releases is not None:
			for release in releases:
				for group in r1["torrentgroup"]:
					if c.releases[group["releaseType"]].lower() == release:
						console.print("Release name: " + html.unescape(group["groupName"]))
						console.print("Release type: " + c.releases[group["releaseType"]])
						console.print("")

def stats():
	stats_action = {"action": "index"}
	r1 = make_request(stats_action).json()["response"]
	t = Table(title=colored(r1["username"], "green"), show_header = False)
	t.add_row("Class", r1["userstats"]["class"])
	t.add_row("Ratio", str(r1["userstats"]["ratio"]))
	t.add_row("Required Ratio", str(r1["userstats"]["requiredratio"]))
	t.add_row("Upload", str(sizeof_fmt(r1["userstats"]["uploaded"])))
	t.add_row("Download", str(sizeof_fmt(r1["userstats"]["downloaded"])))
	t.add_row("Messages", str(colored(r1["notifications"]["messages"], "green") if r1["notifications"]["messages"] != 0 else r1["notifications"]["messages"]))
	console.print(t)

def inbox():
	inbox_action = {"action": "inbox"}
	r1 = make_request(inbox_action).json()["response"]
	t = Table("Sender", "Subject", "Message ID", title=colored("Inbox", "green"))
	for item in r1["messages"]:
		if item["senderId"] == 0:
			sender = "SYSTEM"
		else:
			sender = html.unescape(item["username"])
		subject = html.unescape(item["subject"])
		if item["unread"] == True:
			subject = colored("*", "green") + " " + subject
		t.add_row(sender, subject, str(item["convId"]))
	console.print(t)

def torrent_download(dir, torrentid, fl):
	torrent_action = {"action": "torrent", "id": torrentid}
	r1 = make_request(torrent_action)
	album = r1.json()["response"]["group"]["name"]
	artist = str((r1.json()["response"]["group"]["musicInfo"]["artists"][0]["name"]))
	download_action = {"action": "download", "id": torrentid, "usetoken": int(fl)} if fl == True else {"action": "download", "id": torrentid}
	r2 = make_request(download_action)
	path = dir + artist + " - " + album + ".torrent"
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
					console.print(str(n) + ") " + r["groupName"])
				else:
					console.print(str(n) + ") " + str(r["artist"]) + " - " + str(r["groupName"]))
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