#!/usr/bin/env python

import lyricsgenius


class Lyrics(lyricsgenius.Genius):
    def __init__(self, args):
        super().__init__(args['client_access_token'])

    def get_lyrics(self, artist=None, title=None):
        if artist is not None and title is not None:
            song = self.search_song(title, artist)
            if song is not None:
                self.lyrics = song.lyrics
            else:
                self.lyrics = "NOT FOUND"
        return self.lyrics
