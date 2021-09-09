import actions
import sys

POSSIBLE_ACTIONS = [
	"search",
	"stats",
	"download"
]

def print_possible_actions():
	print("Possible actions:")
	for action in POSSIBLE_ACTIONS:
		print(action)


if len(sys.argv) == 1:
	print("Usage: python3 red.py <action>")
	print_possible_actions()
	sys.exit()

if sys.argv[1] not in POSSIBLE_ACTIONS:
	print_possible_actions()
	sys.exit()

action = sys.argv[1].lower()

if action == "search":
	if len(sys.argv) not in [3, 4]:
		print(f"Usage: python3 red.py {action} <artist> [<album>]")
		sys.exit()
	artist = sys.argv[2].lower()
	if len(sys.argv) == 3:
		print(f"Searching for artist: {artist}")
		actions.artist_search()
	else:
		album = sys.argv[3].lower()
		print(f"Searching for artist: {artist} and album: {album}")
		actions.album_search()

if str(sys.argv[1]).lower() == "stats":
    actions.user_stats()

if str(sys.argv[1]).lower() == "download":
	actions.torrent_download()
