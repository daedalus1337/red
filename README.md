# red search tool

Hello!  I made this command line tool so I didn't have to go to the RED website in order to search for and download torrents.  I personally set up an alias so I can type `red search ARTIST_NAME` right into the terminal and get the info I wanted.  Pretty neat in my opinion.  One thing to keep in mind is that by default, this will only show FLAC files, and it will only show CD and Web releases.  This can be changed using flags; see below.

Here's how it works:

## setup

You will need to add two variables to a .env file:
- `KEY="RED_API_KEY"`
- `FILE_DIR="/Path/to/Downloads/"`

## usage

1. search
	- Artist search:

		In order to search, just run `red.py search ARTIST_NAME`.  It will return a list of album names and release types (album, single, EP, etc.).  Multi-word artist and album names need to be enclosed in quotes!

	- Album search:
		- To search for an album, run `red.py search ARTIST_NAME ALBUM_NAME`.  It will then list the torrent Id, group ID (album ID), media type (CD, web, etc.), size, and amount of seeders of each available download. It will also make a note if the torrent is 24-bit.  Multi-word artist and album names need to be enclosed in quotes!
		- `-m` allows you to filter by media types.  By default, the script only shows CD and WEB.  By adding the `-m` flag, you can look for one or more others. For example, `red.py search ARIST_NAME ALBUM_NAME -m cd vinyl` will show all CD and Vinyl releases.
		- `-f` allows you to filter by format.  By default, the script only shows FLAC releases.  By adding the `-f` flag, you can look for one or more other formats.  For example, `red.py search ARTIST_NAME ALBUM_NAME -f flac mp3 aac` will show all flac, mp3, and aac releases.
		- you CAN use `-m` and `-f` together to find more precise results. For example, `red.py search ARTIST_NAME ALBUM_NAME -m cd -f mp3` will only show mp3 formatted copies of only CD releases.
2. download
	- I built this function on the idea that I would have done an album search before.  After you retrieve the torrent ID from the album search, run `red.py download TORRENT_ID`.  This will save the torrent file (artist - album.torrent) to the directory specified in the .env file. You can also add the `-fl` flag to the end of this command to use a freeleech token. 
3. stats
	- run `red.py stats`, and you will see:
		- Username
		- Class
		- Ratio
		- Required Ratio
		- Upload
		- Download
		- Messages


Also, a huge thank you to my new friend Protsaq for his amazing contributions.