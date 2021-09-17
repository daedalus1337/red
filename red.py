import actions
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='Functions')
parser_1 = subparsers.add_parser('search', help='...')
parser_1.add_argument('artist', type=str, help='...')
parser_1.add_argument("album", type=str, help='album', nargs="?")
parser_1.set_defaults(command="search")

parser_2 = subparsers.add_parser('stats', help='...')
parser_2.add_argument('stats', action="store_true", help='...')
parser_2.set_defaults(command="stats")

parser_3 = subparsers.add_parser('download', help='...')
parser_3.add_argument('torrentid', type=int, help='...')
parser_3.add_argument('groupid', type=int, help='...', nargs="?")
parser_3.add_argument("-fl", action="store_true")
parser_3.set_defaults(command="download")

args = parser.parse_args()

if args.command.lower() == "search":
	if args.album == None:
		actions.artist_search(args.artist.lower())
	if args.album != None:
		actions.album_search(args.artist.lower(), args.album.lower())
if args.command.lower() == "stats":
    actions.user_stats()
if args.command.lower() == "download":
	actions.torrent_download(args.torrentid, args.groupid, args.fl)