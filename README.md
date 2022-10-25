# red search tool

Hello!  I made this command line tool so I didn't have to go to the RED website in order to search for and download torrents.  I personally set up an alias so I can type `red search ARTIST_NAME` right into the terminal and get the info I wanted.  Pretty neat in my opinion.  One thing to keep in mind is that by default, this will only show FLAC files, and it will only show CD and Web releases.  This can be changed using flags; see below.

Here's how it works:

## setup

- Rename the `sample_config.json` file to `config.json`.
- add your API key to the `key` variable
- the `file_dir` variable is the absolute path where your torrent files will download to.
- set the `defaults` variables as you please.  This will filter your search results without the need for flags
- setting the `freeleech` variable to true will automatically use a freeleech token when you download a torrent file

## usage

1. search
	- Artist search:

		In order to search, just run `red.py search ARTIST_NAME`.  It will return a list of album names and release types (album, single, EP, etc.).  Multi-word artist and album names need to be enclosed in quotes!

	- Album search:
		- To search for an album, run `red.py search ARTIST_NAME ALBUM_NAME`.  It will then list the torrent Id, group ID (album ID), media type (CD, web, etc.), size, and amount of seeders of each available download. It will also make a note if the torrent is 24-bit.  Multi-word artist and album names need to be enclosed in quotes!
		- `-m` allows you to filter by media types.  By adding the `-m` flag, you can look for one or more others. For example, `red.py search ARIST_NAME ALBUM_NAME -m cd vinyl` will show all CD and Vinyl releases.  In the config file, you can set `media` to a list of media types you would like to see by default.  If you set it to `['cd', 'web']`, then running `red.py search ARTIST_NAME ALBUM_NAME` will always show cd and web releases only.
		- `-f` allows you to filter by format.  By adding the `-f` flag, you can look for one or more other formats.  For example, `red.py search ARTIST_NAME ALBUM_NAME -f flac mp3 aac` will show all flac, mp3, and aac releases.  In the config file, you can set `format` to a list of formats you would like to see by default.  If you sets it to `['flac']`, then running `red.py search ARTIST_NAME ALBUM_NAME` will only show FLAC results.
		- you CAN use `-m` and `-f` together to find more precise results. For example, `red.py search ARTIST_NAME ALBUM_NAME -m cd -f mp3` will only show mp3 formatted copies of only CD releases.
2. download
	- I built this function on the idea that I would have done an album search before.  After you retrieve the torrent ID from the album search, run `red.py download TORRENT_ID`.  This will save the torrent file (artist - album.torrent) to the directory specified in the config file. If you specify `freeleech=True` in the config file, then it will automatically attempt to use a freeleech token when you download a torrent.  If you specify it as false, you can can add the `-fl` flag to the end of the command to manually use a freeleech token. 
3. stats
	- run `red.py stats`, and you will see:
		- Username
		- Class
		- Ratio
		- Required Ratio
		- Upload
		- Download
		- Messages
4. top lists
	- run `red.py top` to view the top torrents lists
		- you then can select which list you'd like to see
	- the limit is in the config.json.  you can set the limit to 10, 100, and 250

Also, a huge thank you to my new friend Paotsaq for his amazing contributions.