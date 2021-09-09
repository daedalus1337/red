#!/usr/bin/env python3

import key
import sys
import requests

url = "https://redacted.ch/ajax.php?"
header = {"Authorization": key.api_key}

#incomplete.  API only provides integer, so I'm stuck having to manually add these as I identify them.
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
	1022: "Composition",
	1024: "Guest Appearance"
}

def sizeof_fmt(num, suffix='B'):
	for unit in ['','K','M','G','T','P','E','Z']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

def artist_search():
	""" requires 2 arguments """
	artist = {"action": "artist", "artistname": str(sys.argv[2]).lower()}
	r1 = requests.get(url, params=artist, headers=header)
	r1_json = r1.json()['response']

	print("")
	for group in r1_json['torrentgroup']:
		print("Album name: " + group['groupName'])
		print("Release type: " + releases[group['releaseType']])
		print("")

def album_search():
	artist = {"action": "artist", "artistname": str(sys.argv[2]).lower()}
	r1 = requests.get(url, params=artist, headers=header)
	r1_json = r1.json()['response']
	for group in r1_json['torrentgroup']:
		if group['groupName'].lower() == str(sys.argv[3]).lower():
			album = {"action": "torrentgroup", "id": str(group['groupId'])}
			r2 = requests.get(url, params=album, headers=header)
			r2_json = r2.json()['response']
			for release in r2_json['torrents']:
				if release['format'] == "FLAC":
					if release['media'] != "Vinyl":
						if release['encoding'] == '24bit Lossless':
							print("***THIS IS A 24-BIT RELEASE***")
						print("Torrent ID: " + str(release['id']))
						print("Group ID: " + str(group['groupId']))
						print("Media: " + release['media'])
						print("Size: " + str(sizeof_fmt(release['size'])))
						print("Files: " + str(release['fileCount']))
						print("Seeders: " + str(release['seeders']))
						print("")
		else:
			continue

def torrent_download():
	torrentID = {"action": "download", "id": sys.argv[2]}
	r1 = requests.get(url, params=torrentID, headers=header)
	try:
		if len(sys.argv[3]) > 0:
			groupID = {"action": "torrentgroup", "id": sys.argv[3]}
			r2 = requests.get(url, params=groupID, headers=header)
			r2_json = r2.json()['response']
			album = str((r2_json['group']['name']))
			artist = str((r2_json['group']['musicInfo']['artists'][0]['name']))
			open(artist + " - " + album + '.torrent', 'wb').write(r1.content)
	except:
		open('file.torrent', 'wb').write(r1.content)
		print("test")

def user_stats():
    stats = {"action": "index"}
    r1 = requests.get(url, params=stats, headers=header)
    r1_json = r1.json()['response']
    print("Username........." + r1_json['username'])
    print("Class............" + r1_json['userstats']['class'])
    print("Ratio............" + str(r1_json['userstats']['ratio']))
    print("Required Ratio..." + str(r1_json['userstats']['requiredratio']))
    print("Upload..........." + str(sizeof_fmt(r1_json['userstats']['uploaded'])))
    print("Download........." + str(sizeof_fmt(r1_json['userstats']['downloaded'])))
    print("Messages........." + str(r1_json['notifications']['messages']))
