import actions
import const as c
import typer
from typing import List, Optional
from rich.console import Console
from rich.text import Text
import sys
import os
import configurator

console = Console(highlight=False)

freeleech = False
toplist_limit = 10

app = typer.Typer()

try:
    config = actions.load_config()
    configured = True
except Exception:
    configured = False

actions.check_env()

@app.command()
def key():
    actions.register_key()

@app.command()
def configure(
    format: Optional[List[str]] = actions.default_format if configured == True else [],
    media: Optional[List[str]] = actions.default_media if configured == True else [],
    release: Optional[List[str]] = actions.default_release if configured == True else [],
    limit: int = actions.toplist_limit if configured == True else 10,
    freeleech: bool = actions.freeleech if configured == True else False,
    file_dir: str = actions.file_dir if configured == True else ""
):
    configurator.main(release, format, media, limit, freeleech, file_dir)    

@app.command()
def search(
        artist: str = typer.Argument(...),
        album: Optional[str] = typer.Option(None),
        release: Optional[List[str]] = typer.Option(c.release_list if configured == False else actions.default_release),
        media: Optional[List[str]] = typer.Option(c.media_list if configured == False else actions.default_media),
        format: Optional[List[str]] = typer.Option(c.format_list if configured == False else actions.default_format)
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
        console.print(Text("Please run 'red.py configure' to configure your system.", style="red"))
        sys.exit()
    elif configured == True:
        file_dir = actions.file_dir
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
