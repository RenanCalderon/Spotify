import pandas as pd
import json
from sqlalchemy import create_engine

# with open("playlists_2023-02-03.json") as playlist:
#     playlists = json.load(playlist)

engine = create_engine('postgresql://postgres:20hz_20khz@localhost/Musica')


def sp_playlistdf(playlists, save=False):

    columns_playlist = ["id", "name", "spotify_url", "followers", "collaborative", "description", "uri"]
    df = pd.DataFrame(columns=columns_playlist)

    for pl in playlists:
        new_row = {"id": pl["id"], "name": pl["name"], "spotify_url": pl["external_urls"]["spotify"],
                   "followers": pl["followers"]["total"], "collaborative": pl["collaborative"],
                   "description": pl["description"], "uri": pl["uri"]}
        df = pd.concat([df, pd.DataFrame([new_row])])

    if save:
        df.to_sql('playlist', engine, if_exists='replace', index=False)

    return df


def sp_pltracksdf(playlists, save=False):
    columns_tracks = ["id", "name", "artist", "popularity", "id_playlist", "url"]
    df = pd.DataFrame(columns=columns_tracks)

    for pl in playlists:
        id_playlist = pl["id"]
        for trk in pl["tracks"]["items"]:
            tracks = trk["track"]
            new_row = {"id": tracks["id"], "name": tracks["name"],
                       "artist": ', '.join([name["name"] for name in tracks["artists"]]),
                       "popularity": tracks["popularity"],
                       "id_playlist": id_playlist,
                       "url": tracks["external_urls"]["spotify"]}

            df = pd.concat([df, pd.DataFrame([new_row])])

    if save:
        df.to_sql('tracks', engine, if_exists='replace', index=False)

    return df


playlist_df = sp_playlistdf(playlists)
tracks = sp_pltracksdf(playlists)
