import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import cred
from cred import ARCHIVE, PLAYLIST

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-library-read playlist-modify-public",
        client_id=cred.client_id,
        client_secret=cred.client_secret,
        redirect_uri="http://localhost:8888/callback",
    )
)


def show_tracks(results):
    for item in results["items"]:
        track = item["track"]
        added_at = item["added_at"]
        print("%32.32s %s" % (track["artists"][0]["name"], track["name"]))
        # print(track.keys())
        # print(datetime.datetime.fromisoformat(added_at))


def show_p(playlists):
    for item in playlists["items"]:
        print(item)
        # id = ite


# while results["next"]:
#     results = sp.next(results)
#     show_tracks(results)


def main():
    # for each user
    #   create client
    #   last_week_likes = get last week's likes URIs
    #   from current PLAYLIST, move user's tracks to ARCHIVE
    #   put last_week_likes in PLAYLIST <-- limit number? trickle down?

    results = sp.current_user_saved_tracks(limit=15)

    track = results["items"][0]["track"]
    print(track.keys())
    sp.playlist_add_items(PLAYLIST, [track["uri"]])


if __name__ == "__main__":
    main()
