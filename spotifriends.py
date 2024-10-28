import datetime
import pytz

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import cred
from cred import ARCHIVE, PLAYLIST
import server
from log import logger

LIMIT_ADD = 10


def show_tracks(results):
    if "items" in results:
        results = results["items"]
    for item in results:
        if "track" in item:
            item = item["track"]
        logger.debug("%32.32s %s" % (item["artists"][0]["name"], item["name"]))


def move_existing_to_archive(sp):
    items = sp.playlist_items(PLAYLIST)["items"]
    # todo while items.next() items
    tomove = []  # [{uri,loc}, {uri2,loc2}...]
    for i, item in enumerate(items):
        track = item["track"]
        if item["added_by"]["id"] == sp.me()["id"]:
            tomove.append({"uri": track["uri"], "positions": [i]})
    if tomove:  # empty list == false in python | tomove is a list
        logger.debug(f"user {sp.me()['display_name']} - moving to archive")
        sp.playlist_remove_specific_occurrences_of_items(PLAYLIST, tomove)
        sp.playlist_add_items(ARCHIVE, [i["uri"] for i in tomove])


utc = pytz.UTC


def get_days():
    "returns monday and sunday of last week"
    today = datetime.datetime.today().replace(
        tzinfo=utc, hour=0, minute=0, second=0, microsecond=0
    )
    days_since = today.weekday() + 7
    monday = today - datetime.timedelta(days=days_since)
    # logger.debug(f"{today} - {monday} - {monday + datetime.timedelta(days=6)}")
    return monday, monday + datetime.timedelta(days=6)


def add_last_likes_to_playlist(sp):
    liked_tracks = sp.current_user_saved_tracks(limit=LIMIT_ADD)
    logger.debug(
        f"user {sp.me()['display_name']} - {len(liked_tracks)} max liked"
    )  # HELP DON'T KNOW WHY IT GIVES 7
    # show_tracks(liked_tracks)
    monday, sunday = get_days()
    last_liked = []
    for item in liked_tracks["items"]:
        if sunday > datetime.datetime.fromisoformat(item["added_at"]) >= monday:
            last_liked.append(item["track"])
    logger.debug(f"user {sp.me()['display_name']} - {len(last_liked)} liked last week")

    # show_tracks(last_liked)
    if last_liked:
        sp.playlist_add_items(PLAYLIST, [i["uri"] for i in last_liked])


def main():
    tokens = server.load_tokens()
    for id, info in tokens.items():
        logger.debug(f"---------{info['spotify_username']}-----------")
        sp = server.create_spotify_client(id)
        logger.debug(f"---sp----{info['spotify_username']}--created--")
        move_existing_to_archive(sp)
        add_last_likes_to_playlist(sp)
        logger.debug(f"---------{info['spotify_username']}--over-----")
        logger.debug(f"\n\n\n")


if __name__ == "__main__":
    main()
