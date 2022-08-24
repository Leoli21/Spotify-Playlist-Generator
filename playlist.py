class Playlist:
    '''
    The "Playlist" class will represent a Spotify playlist
    '''
    def __init__(self, name, id):
        '''
        :param name (str): Name of the Playlist
        :param id: Spotify Playlist ID
        '''
        self.name = name
        self.id = id

    # Overriding str method to make readable version of
    # a Playlist object
    def __str__(self):
        return f'Playlist: {self.name}'
