import os

from spotifyclient import SpotifyClient

def main():
    # Instantiate Spotify Client class
    spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"), os.getenv("SPOTIFY_USER_ID"))

    # Get user's last played tracks
    users_last_played_tracks = int(input("How many of your past tracks would you like to use for Recommendations? "))
    last_played_tracks = spotify_client.get_last_played_tracks(users_last_played_tracks)

    print(f'\nPresented to you are the last {users_last_played_tracks} tracks you have listened to on Spotify:')
    for index, track in enumerate(last_played_tracks):
        print(f'{index+1}- {track}')

    # Prompt user to choose which tracks they would like to use as seeds to generate the playlist
    track_numbers = input("\nEnter a list of up to 5 tracks that you would like to use as the seeds. Type the track number followed by a space: ")
    track_numbers = track_numbers.split()
    chosen_tracks = [last_played_tracks[int(num)-1] for num in track_numbers]

    # Get the recommended tracks based off of the seed tracks
    recommended_tracks = spotify_client.get_track_recommendations(chosen_tracks)
    print("\nHere are the recommended tracks that will be included in your new playlist:")
    for index, track in enumerate(recommended_tracks):
        print(f'{index+1}- {track}')

    # Prompt the user for what they want to name their playlist containing the recommended tracks
    playlist_name = input("\nWhat will you name the playlist? ")
    playlist = spotify_client.create_playlist(playlist_name)
    print(f"\nPlaylist '{playlist.name}' was successfully created.")

    # Populate the playlist with the recommended tracks
    spotify_client.populate_playlist(playlist, recommended_tracks)
    print(f"\nRecommended tracks successfully uploaded to '{playlist.name}'.")\

if __name__ == "__main__":
    main()


