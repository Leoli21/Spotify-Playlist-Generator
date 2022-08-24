class Track:
    '''
    This "Track" class will represent a piece of music on Spotify.
    '''

    def __init__(self, name, id, artist):
        '''
        :param name (str): Track Name
        :param id (int): Spotify Track ID
        :param artist (str): Artist who composed the track
        '''
        self.name = name
        self.id = id
        self.artist = artist

    # Used to compose a URI that can then be used to communicate
    # with the Spotify Web API
    def create_spotify_uri(self):
        return f'spotify:track:{self.id}'

    # Overriding str method to create a readable version
    # of a track object
    def __str__(self):
        return self.name + " by " + self.artist
