import actions
import os
import json
import const as c
import typer
from typing import List, Optional

filename = os.path.join(os.path.dirname(__file__), 'config.json')
with open(filename) as jsonfile:
    data = json.load(jsonfile)

file_dir = data['file_dir']
default_release = data['defaults']['release']
default_media = data['defaults']['media']
default_format = data['defaults']['format']
freeleech = data['freeleech']
toplist_limit = data['toplist_limit']

app = typer.Typer()

@app.command()
def search(
        artist: str = typer.Argument(...),
        album: Optional[str] = typer.Option(None),
        release: Optional[List[str]] = typer.Option(default_release, help="possible release types:"),
        media: Optional[List[str]] = typer.Option(default_media, help="possible media types:"),
        format: Optional[List[str]] = typer.Option(default_format, help="possible formats:")
):
    actions.search(artist, release, media, format, album)

@app.command()
def stats():
    actions.stats()

@app.command()
def download(
        torrent_id: int = typer.Argument(...),
        fl: bool = typer.Option(False, freeleech)
):
    actions.torrent_download(file_dir, torrent_id, fl)

@app.command()
def top():
    print("choose a list")
    n = 1
    for i in c.top_lists:
        print(str(n) + ") " + c.top_lists[i])
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