import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import cred
from cred import ARCHIVE, PLAYLIST
import server

"""
oggi: proof of concept authentication
objectives: oX
- minimal HTML page with link to spotify auth -> HTML page (o1)
- minimal python server that: -> flask minimal server (o2)
    - serves HTML page
    - accept callback from spotify to save token
- open port with ngrok -> install ngrok and open ports (o3)

obbiettivo: autenticare un utente (nuovo) su una webapp/servizio (spotifriends.com) che usa il tuo spotify
1. user pp apri spotifriends.com
2. clicchi un link che dice "autenticati su spotify"
3. questo link ti porta a una pagina DI SPOTIFY, che ti chiede se ti va bene dare accesso a spotifriends
4. quando clicchi conferma, vieni ridirezionato a spotifriends.com/callback:
    redirect to https://www.spotifriends.com/callback?token=THISISMYC0MPL3XT0K3N
    so spotifriends.com receives a GET (probably) request with param token
5. spotifriends, for all successive calls to spotify API for user pp, passes token with each request, until token is not valid anymore and authentication is requested again (error 40X: unauthorized, re-authorize)


"""


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
    tokens = server.load_tokens()
    for id, info in tokens.items():
    #   last_week_likes = get last week's likes URIs
        print(f"-------{info['spotify_username']}---------")
        sp = spotipy.Spotify(auth=info['access_token'])
        results = sp.current_user_saved_tracks(limit=15)
    #   put last_week_likes in PLAYLIST <-- limit number? trickle down?
    #   from current PLAYLIST, move user's tracks to ARCHIVE

        show_tracks(results)
        print(f'\n\n\n')

    # track = results["items"][0]["track"]
    # print(track.keys())
    # sp.playlist_add_items(PLAYLIST, [track["uri"]])


if __name__ == "__main__":
    main()
