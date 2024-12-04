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
	15: "Interview",
	16: "Mixtape",
	17: "Demo",
	18: "Concert Recording",
	19: "DJ Mix",
	21: "Unknown",
	1021: "Produced By",
	1022: "Composition",
	1023: "Remixed By",
	1024: "Guest Appearance"
}
release_list = [releases[r] for r in releases]

formats = {
	0: "MP3",
	1: "FLAC",
	2: "AAC",
	3: "AC3",
	4: "DTS"
}
format_list = [formats[f] for f in formats]

media = {
	0: "CD",
	1: "DVD",
	2: "Vinyl",
	3: "Soundboard",
	4: "SACD",
	5: "DAT",
	6: "Cassette",
	7: "WEB",
	8: "Blu-Ray"
}
media_list = [media[m] for m in media]

top_lists = {
	1: "Most Active Torrents Uploaded in the Past Day",
	2: "Most Active Torrents Uploaded in the Past Week",
	3: "Most Active Torrents of All Time",
	4: "Most Snatched Torrents",
	5: "Most Data Transferred Torrents",
	6: "Best Seeded Torrents"
}

top_list_count = [10,100,250]

url = "https://redacted.sh/ajax.php?"

config_json = { 
    "file_dir": "/absolute/path/to/download/location",
    "defaults": {
        "format": [],
        "media": [],
        "release": []
    },
    "freeleech": False,
    "toplist_limit": 10
}
