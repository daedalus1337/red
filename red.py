import actions
import argparse
import sys
import os
import json
import const as c

filename = os.path.join(os.path.dirname(__file__), 'config.json')
with open(filename) as jsonfile:
	data = json.load(jsonfile)

api_key = data['key']
file_dir = data['file_dir']
default_release = data['defaults']['release']
default_media = data['defaults']['media']
default_format = data['defaults']['format']
freeleech = data['freeleech']
toplist_limit = data['toplist_limit']
header = {"Authorization": api_key}

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="Functions")
parser_1 = subparsers.add_parser("search", help='artist/album search')
parser_1.add_argument("artist", type=str, help='artist name')
parser_1.add_argument("-r", help="releases", nargs="+", default=default_release)
parser_1.add_argument("album", type=str, help='album name', nargs="?")
parser_1.add_argument("-m", help="possible media types: cd, dvd, vinyl, soundboard, sacd, dat, cassette, web, blu-ray", nargs="+", default=default_media)
parser_1.add_argument("-f", help="possible formats: flac, mp3, aac, ac3, dts", nargs="+", default=default_format)
parser_1.set_defaults(command="search")

parser_2 = subparsers.add_parser("stats", help="show your RED user stats")
parser_2.add_argument("stats", action="store_true", help="show your RED user stats")
parser_2.set_defaults(command="stats")

parser_3 = subparsers.add_parser("download", help="download a torrent")
parser_3.add_argument("torrentid", type=int, help="torrent ID found in album search")
parser_3.add_argument("-fl", action="store_true", default=freeleech)
parser_3.set_defaults(command="download")

parser_4 = subparsers.add_parser("top", help="shows the top torrents")
parser_4.add_argument("top", action="store_true", help="shows the top torrents")
parser_4.set_defaults(command="top")

args = parser.parse_args()

try:
    args.command
except:
    parser.print_help()
    sys.exit(0)

if args.command.lower() == "search":
	if args.album == None:
		actions.artist_search(args, header)
	if args.album != None:
		actions.album_search(args, header)
if args.command.lower() == "stats":
    actions.user_stats(header)
if args.command.lower() == "download":
	actions.torrent_download(args,file_dir, header)
if args.command.lower() == "top":
	print("choose a list")
	n = 1
	for i in c.top_lists:
		print(str(n) + ") " + c.top_lists[i])
		n += 1
	list = int(input("Enter a number:"))
	actions.top(header, list, toplist_limit)