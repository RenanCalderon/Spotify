# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 20:42:24 2023

@author: Renan
"""

import requests
import base64
import json
import csv

from datetime import datetime


class Spotify:

    def __init__(self, file):
        self.masterToken = ""
        self.getAccessToken(file)

    # Generar Token
    def getAccessToken(self, file):

        authUrl: str = "https://accounts.spotify.com/api/token"
        authHeader = {}
        authData = {}

        # Import json file
        with open(file) as archivo:
            file_json = json.load(archivo)
        # Base Enconde Client ID and Client Secret ID

        message = f"{file_json['clientID']}:{file_json['clientSecret']}"
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        authHeader['Authorization'] = "Basic " + base64_message
        authData['grant_type'] = "client_credentials"

        res = requests.post(authUrl, headers=authHeader, data=authData)

        if res.status_code == 200:

            print("The token request has succeded")
            responseObject = res.json()
            Token = responseObject['access_token']
            self.masterToken = Token
            return Token

        else:
            print("Credentials Error")

    def getPlaylist(self, playlistID, save=False):
        playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}"
        # print(playlistEndPoint)
        getHeader = {
            "Authorization": "Bearer " + self.masterToken
        }

        res = requests.get(playlistEndPoint, headers=getHeader)

        if res.status_code == 200:

            print("The playlist request has been successful")
            playlistObject = res.json()

            if save:
                date_now = datetime.now().strftime('%Y-%m-%d')
                with open(f"{playlistObject['id']}_{date_now}.json", "w") as write_file:
                    json.dump(playlistObject, write_file)

                print("File Saved")

            return playlistObject

        else:

            print("Something went wrong")
            print(res.status_code)

    def getSeveralPlaylist(self, name_file, save=False):

        playlists = []

        with open(f"{name_file}", "r") as playlist:
            reader = csv.reader(playlist)

            for row in reader:
                playlistID = row[1]
                # print(playlistID)
                pl = Spotify.getPlaylist(self, playlistID)
                playlists.append(pl)

        if save:

            date_now = datetime.now().strftime('%Y-%m-%d')
            with open(f"playlists_{date_now}.json", "w") as write_file:
                json.dump(playlists, write_file)
            print("Playlist Saved")

        return playlists
