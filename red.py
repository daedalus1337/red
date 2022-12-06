import actions
import const as c
import typer
from typing import List, Optional
from rich.console import Console
import sys
from termcolor import colored
import os

console = Console(highlight=False)

freeleech = False
toplist_limit = 10

app = typer.Typer()

try:
    config = actions.load_config()
    configured = True
except Exception:
    configured = False

if os.path.isfile(".env"):
    pass
else:
    console.print(colored("Tihs is likely your first run, as you have not registered your API key.", "red"))
    api_key = input("Please enter your API key (or press Ctrl + C to exit): ")
    f = open(".env", "w")
    f.write(f"KEY='{api_key}'")
    f.close()
    

@app.command()
def search(
        artist: str = typer.Argument(...),
        album: Optional[str] = typer.Option(None),
        release: Optional[List[str]] = typer.Option(c.release_list if configured == False else actions.default_release, help="possible release types:"),
        media: Optional[List[str]] = typer.Option(c.media_list if configured == False else actions.default_media, help="possible media types:"),
        format: Optional[List[str]] = typer.Option(c.format_list if configured == False else actions.default_format, help="possible formats:")
):
    actions.search(artist, release, media, format, album)

@app.command()
def stats():
    actions.stats()

@app.command()
def download(
       torrent_id: int = typer.Argument(...),
       fl: bool = typer.Option(freeleech)
):
    if configured == False:
        console.print(colored("Please configure this system in order to download torrents.  Check the readme for more info.", "red"))
        sys.exit()
    elif configured == True:
        file_dir = data["file_dir"]
        actions.torrent_download(file_dir, torrent_id, fl)

@app.command()
def top():
    console.print("choose a list")
    n = 1
    for i in c.top_lists:
        console.print(str(n) + ") " + c.top_lists[i])
        n += 1
    list = int(input("Enter a number:"))
    actions.top(list, toplist_limit)

@app.command()
def inbox():
    actions.inbox()

@app.command()
def read(
    message_id: str = typer.Argument(...)
):
    actions.read(message_id)

if __name__ == "__main__":
    app()
