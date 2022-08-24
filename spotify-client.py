import json

import requests

from track import Track
from playlist import Playlist

class SpotifyClient:
    '''
    This class will perform the input/output operations using the Spotify
    Web API
    '''
    def __init__(self, authorization_token, user_id):
        '''
        :param authorization_token (str): Spotify API Token that will be fethced directly from Spotify website
        :param user_id (int): Spotify User ID
        '''

    # Fetches the last 'n' played tracks of current user
    def get_last_played_tracks(self, limit = 10):
        '''
        :param limit (int): Number of tracks to get. This value should be <= 50
        :return tracks (a list containing tracks): List of last played tracks
        '''
        url = f'https://api.spotify.com/v1/me/player/recently-played?limit={limit}'


        response = self._place_get_api_request(url)

        # Getting back a response with all the different last played tracks
        response_json = response.json()

        # Unpacking the data for the last played tracks and create a list of those tracks
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for track in response_json["items"]]
        return tracks

    # Get a list of recommended tracks based upon the listed seed tracks
    def get_track_recommendations(self, seed_tracks, limit = 50):
        '''
        :param seed_tracks (list of Track objects): Reference tracks that will be used to get recommendations. Should be 5 or less
        :param limit (int): Number of recommended tracks to be returned
        :return tracks (list of Track objects): List of the recommended tracks
        '''
        seed_tracks_url = ""
        for track in seed_tracks:
            seed_tracks_url += track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f'https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}'
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for track in response_json["tracks"]]
        return tracks

    # Creates a playlist with given name from user
    def create_playlist(self, name):
        '''
        :param name (str): Name of the playlist
        :return playlist (Playlist): A newly created Playlist object
        '''
        data = json.dumps({
            "name": name,
            "description": "Recommended tracks",
            "public": True
        })
        url = f'https://api.spotify.com/v1/users/{self._user_id}/playlists'
        response = self._place_post_api_request(url, data)
        response_json = response.json()

        # Create the actual Playlist object
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    # Add recommended tracks to the playlist
    def populate_playlist(self, playlist, tracks):
        '''
        :param playlist (Playlist): Playlist that we will add the recommmended tracks to
        :param tracks (list of Track objects): Tracks that will be added to the Playlist
        :return response: API response
        '''
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f'https://api.spotify.com/v1/playlists/{playlist.id}/tracks'
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        return response_json


    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data = data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {self.authorization_token}'
            }
        )
        return response
    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {self._authorization_token}'
            }
        )
        return response
