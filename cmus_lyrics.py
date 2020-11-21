#!/usr/bin/env python

from cmus import CmusPlayer
from settings import Settings
import lyricsgenius
import os
import sys


class Lyrics(lyricsgenius.Genius):
    def __init__(self, args):
        super().__init__(args['client_access_token'])

    def get_lyrics(self, artist=None, title=None):
        if artist is not None and title is not None:
            song = self.search_song(title, artist)
            if song is not None:
                self.lyrics = song.lyrics
            else:
                self.lyrics = None
        return self.lyrics


class Main:

    def __init__(self, CmusPlayer):
        self.cms = CmusPlayer
        if (self.cms.is_cmus_playing()):
            self.cms.get_tags()


if __name__ == '__main__':
    cm = CmusPlayer()

    # TODO
    # arguments like:
    # - credential file
    # - destination folder for lyrics (same as song or generic)
    # save lyrics to folder + format
    # read lyrics if exists

    try:
        s = Settings()
        s.get_settings()
        lyrics = Lyrics(s.settings)

    except Exception as e:
        sys.exit(e)

    main = Main(cm)
    if (main.cms.is_cmus_playing()):
        tags = main.cms.tags
        lyrics_text = lyrics.get_lyrics(tags.artist, tags.title)

    """ print lyrics """
    with open("/tmp/cml.txt", "w") as fo:
        fo.write(lyrics_text)

    os.system("less /tmp/cml.txt")
