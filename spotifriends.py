import datetime
import pytz

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import cred
from cred import ARCHIVE, PLAYLIST
import server
import logging

logger = logging.getLogger(__name__)
LIMIT_ADD = 10


def show_tracks(results):
    for item in results["items"]:
        track = item["track"]
        added_at = item["added_at"]
        print("%32.32s %s" % (track["artists"][0]["name"], track["name"]))
        # print(track.keys())
        # print(datetime.datetime.fromisoformat(added_at))


def move_existing_to_archive(sp):
    logger.info(f"removing songs from user {sp.me()}")
    items = sp.playlist_items(PLAYLIST)["items"]
    # todo while items.next() items
    tomove = []  # [[uri,loc], [uri2,loc2]...]
    for i, item in enumerate(items):
        track = item["track"]
        if item["added_by"]["id"] == sp.me()["id"]:
            tomove.append({"uri": track["uri"], "positions": [i]})
    if tomove:
        sp.playlist_remove_specific_occurrences_of_items(PLAYLIST, tomove)
        sp.playlist_add_items(ARCHIVE, [i["uri"] for i in tomove])


utc = pytz.UTC


def add_last_likes_to_playlist(sp):
    last_likes = [
        i["track"]
        for i in sp.current_user_saved_tracks(limit=LIMIT_ADD)["items"]
        if datetime.datetime.fromisoformat(i["added_at"])
        < datetime.datetime.today().replace(tzinfo=utc) - datetime.timedelta(days=7)
    ]
    sp.playlist_add_items(PLAYLIST, [i["uri"] for i in last_likes])


def main():
    tokens = server.load_tokens()
    print([(id, info["spotify_username"]) for id, info in tokens.items()])
    big_test = None
    for id, info in tokens.items():
        print(f"-------{info['spotify_username']}---------")
        sp = server.create_spotify_client(id)
        # if info["spotify_username"] == "pollomarzo":
        #     big_test = sp.current_user_saved_tracks(limit=LIMIT_ADD)["items"][0]
        # else:
        #     print(big_test.keys())
        #     print(big_test["track"].keys())
        #     print(big_test["track"]["uri"])
        #     sp.playlist_add_items(PLAYLIST, [big_test["track"]["uri"]])
        #     print("FUCK YES")
        move_existing_to_archive(sp)
        add_last_likes_to_playlist(sp)
        show_tracks(sp.current_user_saved_tracks(limit=LIMIT_ADD))
        continue
        # sp.get_user_token(id)

        add_last_likes_to_playlist(sp)
        print(f"for user {info['spotify_username']}")
        # show_tracks(results)
        print(f"\n\n\n")

    # track = results["items"][0]["track"]
    # print(track.keys())
    # sp.playlist_add_items(PLAYLIST, [track["uri"]])


if __name__ == "__main__":
    main()
