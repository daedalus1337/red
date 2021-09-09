# red search tool


Disclaimer: this is the first code I have ever shared with anyone.  I’m sure it can be done better by someone with more experience, but it does fit my individual needs.  Suggestions are more than welcome, although I don’t know if I’ll have time to improve this though.  Anyway…

Hello!  I made this command line tool so I didn't have to go to the RED website in order to search for and download torrents.  I personally set up an alias so I can type `red search ARTIST_NAME` right into the terminal and get the info I wanted.  Pretty neat in my opinion.  A couple of things to keep in mind are that this will only show FLAC files, and it will NOT show vinyl rips.  This can be changed, but those were two solid parameters that I never deviate from, so I didn't see why I shouldn't hardcode them.

Here's how it works:

setup:

In the same directory as the script, you will need a separate file called `key.py`.  In that file simply add `api_key="YOUR_API_KEY_HERE"`.  It needs to be a string, so keep it in the quotes.  On line 81, you can add the path and/or change the filename to something you can identify.  Eventually, I'll update this so it automatically saves the file as artist-album.torrent, but for my own use, that function is irrelevant.

usage:

1. search
	1. Artist search:

	In order to search, just run `red.py search ARTIST_NAME`.  It will return a list of album names and release types (album, single, EP, etc.).  Multi-word artist and album names need to be enclosed in quotes!

	1. Album search:
		2. To search for an album, run `red.py search ARTIST_NAME ALBUM_NAME`.  It will then list the torrent Id, group ID (album ID), media type (CD, web, etc.), size, and amount of seeders of each available download. It will also make a note if the torrent is 24-bit.  Multi-word artist and album names need to be enclosed in quotes!
2. download
	1. I built this function on the idea that I would have done an album search before.  After you retrieve the torrent ID from the album search, run `red.py download TORRENT_ID`.  This API call only returns the file without any naming information, so I added the group ID to the album search, and if you run `red.py download TORRENT_ID GROUP_ID`, it will properly name the file "ARTIST - ALBUM.torrent".
3. stats
	1. run `red.py stats`, and you will see:
		2. Username
		3. Class
		4. Ratio
		5. Required Ratio
		6. Upload
		7. Download
		8. Messages
