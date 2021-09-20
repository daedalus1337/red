import actions
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="Functions")
parser_1 = subparsers.add_parser("search", help='artist/album search')
parser_1.add_argument("artist", type=str, help='artist name')
parser_1.add_argument("album", type=str, help='album name', nargs="?")
parser_1.add_argument("-m", help="possible media types: cd, dvd, vinyl, soundboard, sacd, dat, cassette, web, blu-ray", nargs="+", default=["cd", "web"])
parser_1.add_argument("-f", help="possible formats: flac, mp3, aac, ac3, dts", nargs="+", default=["flac"])
parser_1.set_defaults(command="search")

parser_2 = subparsers.add_parser("stats", help="show your RED user stats")
parser_2.add_argument("stats", action="store_true", help="show your RED user stats")
parser_2.set_defaults(command="stats")

parser_3 = subparsers.add_parser("download", help="download a torrent")
parser_3.add_argument("torrentid", type=int, help="torrent ID found in album search")
parser_3.add_argument("-fl", action="store_true")
parser_3.set_defaults(command="download")

args = parser.parse_args()

if args.command.lower() == "search":
	if args.album == None:
		actions.artist_search(args.artist.lower())
	if args.album != None:
		actions.album_search(args.artist.lower(), args.album.lower(), args.m, args.f)
if args.command.lower() == "stats":
    actions.user_stats()
if args.command.lower() == "download":
	actions.torrent_download(args.torrentid, args.fl)