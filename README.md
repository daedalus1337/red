# red search tool

Hello!  I made this command line tool so I didn't have to go to the RED website in order to search for and download torrents.  I personally set up an alias so I can type `red search ARTIST_NAME` right into the terminal and get the info I wanted.  Pretty neat in my opinion.

Here's how it works:

## setup

- To install the dependencies, run `pip install -r requirements.txt`.
- Try running any command.  The application will detect that you have not registered an API key, and it will prompt you to enter it in.  It will create a `.env` file for you, so you don't even have to worry about it.
- Most other functions will work without any further configuration.  However, I do recommend reading the next section to learn more about configuration.

## commands

1. Configure
	- The goal for the configurator is to set up specific default settings to personalize your search experience.  It allows you to configure the folowing search filters as defaults so you do not need to manually specify them every time you search:
		- release types
		- media types
		- formats
	- Other settings include:
		- download directory: this is required for the `download` function to work.  All torrent files will download to this directory.
		- freeleech: if you say `yes` to this, then the application will automatically try to use a freeleech token when you download a torrent file.  If you have no available tokens, or if the torrent is larger than 2GB, it will still download as normal, and it will not raise any errors.
		- "top" list limit: this limit allows you to choose if you want to see the first 10, 100, or 250 torrents in any of the "top" lists.  Obviously, the higher the number, the longer it will take for the results to load.
2. Search
	- Artist search:

		- In order to search, just run `python red.py search ARTIST_NAME`.  It will return a list of album names and release types (album, single, EP, etc.).  Multi-word artist and album names need to be enclosed in quotes!
		- The `--release` flag will allow you to manually declare what release types you want to see.  You can use it more than once.  For example `python red.py search ARTIST_NAME --release Album --release EP`.  It is case sensitive for now.

	- Album search:
		- To search for an album, run `python red.py search ARTIST_NAME --album ALBUM_NAME`.  It will then list the torrent Id, group ID (album ID), media type (CD, web, etc.), size, and amount of seeders of each available download. Multi-word artist and album names need to be enclosed in quotes!
		- The `--media` flag allows you to manually filter only the media types you want to see. For example, `red.py search ARIST_NAME --album ALBUM_NAME --media CD` will show all CD releases.  This flag can be used multiple times.  For example `python red.py search ARTIST_NAME --album ALBUM_NAME --media --media CD --media Vinyl`.  It is case sensitive for now.
		- The `--format` allows you to manually filter by format.  For example, `python red.py search ARTIST_NAME --album ALBUM_NAME --format FLAC` will show all flac versions of the album.  This flag can be used multiple times.  For example `python red.py search ARTIST_NAME --album ALBUM_NAME --format FLAC --format MP3`.  It is case sensitive for now.
		- You CAN use `--media` and `--format` flags together to find more precise results. For example, `python red.py search ARTIST_NAME --album ALBUM_NAME --media CD --format MP3` will only show MP3 copies of only CD releases.
3. Download
	- I built this function on the idea that I would have done an album search before.  After you retrieve the torrent ID from the album search, run `python red.py download TORRENT_ID`.  This will save the torrent file (`ARTIST_NAME - ALBUM_NAME.torrent`) to the directory you specified in the configurator.
	- You can use the `--freeleech` flag to specify if the download function should try to use a freeleech token.  For example, `python red.py download XXXXX --freeleech`.
	- It seems worth noting that this is the only function that specifically requires that the configurator be run already because it needs to know what file path you want your torrent files to download to.
4. Stats
	- Run `python red.py stats`, and you will see:
		- Username
		- Class
		- Ratio
		- Required Ratio
		- Upload
		- Download
		- Unread Messages (will be highlighted green if you have more than 0)
5. Top Lists
	- Run `python red.py top` to view the top torrents lists
		- you then can select which list you'd like to see
	- You can set the limit to 10, 100, or 250 in the configurator
6. Inbox
	- Run `python red.py inbox` to view your inbox
	- It will show the sender, the subject, and the message ID in a pretty badass table
	- Unread messages will be highlighted green.
7. Read
	- If you want to read a message from your inbox, copy the message ID and run this command: `python red.py read messageID`
	- It will show the entire correspondence of that conversation in a table.  There is no way to sort it, or show only one, or anything beyond what you see when you run the intial command.  I'm open to suggestion though.

## roadmap
- messaging: I'll probably be adding the ability to send messages, but I'm lazy right now.
