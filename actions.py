import requests
import html
import sys
import const as c
from prettytable import PrettyTable, ALL
import os
from termcolor import colored, cprint


def make_request(params, header):
	req = requests.get(c.url, params=params, headers=header)
	if req.status_code != 200:
		print(f"Status of request is {req.status_code}. Aborting...")
		print(req._content)
		sys.exit()
	return req


def sizeof_fmt(num, suffix="B"):
	for unit in ["","K","M","G","T","P","E","Z"]:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, "Yi", suffix)


def print_album_info(release):
	print("Torrent ID: " + str(release["id"]))
	print("Media: " + release["media"])
	print("Format: " + release["format"])
	print("Encoding: " + release["encoding"])
	print("Size: " + str(sizeof_fmt(release["size"])))
	print("Files: " + str(release["fileCount"]))
	print("Seeders: " + str(release["seeders"]))
	print("")


def artist_search(args, header):
	""" requires 2 arguments """
	artist = {"action": "artist", "artistname": args.artist.lower()}
	r1 = make_request(artist, header).json()["response"]
	if args.r is None:
		for group in r1["torrentgroup"]:
			print("Release name: " + html.unescape(group["groupName"]))
			print("Release type: " + c.releases[group["releaseType"]])
			print("")
	elif args.r is not None:
		for release in args.r:
			for group in r1["torrentgroup"]:
				if c.releases[group["releaseType"]].lower() == release:
					print("Release name: " + html.unescape(group["groupName"]))
					print("Release type: " + c.releases[group["releaseType"]])
					print("")


def album_search(args, header):
	artist = {"action": "artist", "artistname": args.artist.lower()}
	r1 = make_request(artist, header).json()["response"]
	for group in r1["torrentgroup"]:
		if html.unescape(group["groupName"].lower()) == args.album.lower():
			group = {"action": "torrentgroup", "id": str(group["groupId"])}
			r2 = make_request(group, header).json()["response"]
			for release in r2["torrents"]:
				if args.f is None and args.m is None:
					print_album_info(release)
				elif args.m is None and args.f is not None:
					if release["format"].lower() in args.f:
						print_album_info(release)
				elif args.f is None and args.m is not None:
					if release["media"].lower() in args.m:
						print_album_info(release)
				elif release["format"].lower() in args.f and release["media"].lower() in args.m:
					print_album_info(release)


def torrent_download(args, dir, header):
	if args.fl is True:
		download_params = {"action": "download", "id": args.torrentid, "usetoken": int(True)}
	else:
		download_params = {"action": "download", "id": args.torrentid}
	details_params = {"action": "torrent", "id": args.torrentid}
	r1 = make_request(details_params, header)
	album = r1.json()["response"]["group"]["name"]
	artist = str((r1.json()["response"]["group"]["musicInfo"]["artists"][0]["name"]))
	download_params = {"action": "download", "id": args.torrentid, "usetoken": int(args.fl)}
	r2 = make_request(download_params, header)
	path = dir + artist + " - " + album + ".torrent"
	open(path, "wb").write(r2.content)
	print(f"Torrent for {artist} - {album} was successfully downloaded!")


def user_stats(header):
	stats_params = {"action": "index"}
	r1 = make_request(stats_params, header).json()["response"]
	print("Username........." + r1["username"])
	print("Class............" + r1["userstats"]["class"])
	print("Ratio............" + str(r1["userstats"]["ratio"]))
	print("Required Ratio..." + str(r1["userstats"]["requiredratio"]))
	print("Upload..........." + str(sizeof_fmt(r1["userstats"]["uploaded"])))
	print("Download........." + str(sizeof_fmt(r1["userstats"]["downloaded"])))
	print("Messages........." + str(r1["notifications"]["messages"]))

def top(header, list, toplist_limit):
	list_params = {"action": "top10", "limit": toplist_limit}
	r1 = make_request(list_params, header).json()["response"]
	for item in r1:
		if item["caption"] == c.top_lists[list]:
			print("---")
			print(item["caption"])
			print("---")
			n = 1
			for r in item["results"]:
				if r["artist"] == False:
					print(str(n) + ") " + r["groupName"])
				else:
					print(str(n) + ") " + str(r["artist"]) + " - " + str(r["groupName"]))
				print("Torrent ID: " + str(r["torrentId"]))
				print("Media: " + r["media"])
				print("Format: " + r["format"])
				print("Encoding: " + r["encoding"])
				print("Size: " + str(sizeof_fmt(r["size"])))
				print("Seeders: " + str(r["seeders"]))
				print("")
				n += 1

def inbox(header):
	inbox_params = {"action": "inbox"}
	r1 = make_request(inbox_params, header)
	r1 = make_request(inbox_params, header).json()["response"]
	t = PrettyTable()
	t.field_names = ["Sender", "Subject", "Message ID"]
	t.hrules = ALL
	t.max_table_width = os.get_terminal_size()[0]-4
	for item in r1["messages"]:
		if item["senderId"] == 0:
			sender = "SYSTEM"
		else:
			sender = html.unescape(item["username"])
		subject = html.unescape(item["subject"])
		if item["unread"] == True:
			subject = colored("*", "green") + " " + subject
		t.add_row([sender, subject, item["convId"]])
	print(t)

def read(header, args):
	read_params = {"action": "inbox", "type": "viewconv", "id": args.messageId}
	r1 = make_request(read_params, header).json()["response"]
	print("")
	print(r1["subject"])
	print("---")
	for item in r1["messages"]:
		print(item["senderName"] + ":")
		print(html.unescape(item["bbBody"]))
		print("")