#!/usr/bin/env python

from cmus import CmusPlayer
from settings import Settings
from lyrics import Lyrics
import os
import sys
import subprocess
import re


class Main:

    def __init__(self, CmusPlayer):
        self.cms = CmusPlayer
        if (self.cms.is_cmus_playing()):
            self.cms.get_tags()

    def print_lyrics(self):
        subprocess.call(["less", self.lyrics_file])

    # +------------------------------------------------------+
    # | set the file path and name removing not alpha chars  |
    # +------------------------------------------------------+

    def set_file(self, path='/tmp'):
        tags = self.cms.tags

        if (not os.path.exists(path) and not os.path.isfile(path)):
            os.mkdir(path)

        # minimize artist name
        artist_folder = re.sub('[\W]+', '', tags.artist) .lower()
        artist_folder = os.path.join(path, artist_folder)
        if (not os.path.exists(artist_folder) and not
                os.path.isfile(artist_folder)):
            os.mkdir(artist_folder)

        # minimize file name
        self.lyrics_file_name = re.sub('[\W]+', '', tags.title) \
                                  .lower() + ".txt"
        self.lyrics_file = os.path.join(path, artist_folder, self.lyrics_file_name)
        return self.lyrics_file

    # +------------------------------------------+
    # | check if lyrics file really exists on fs |
    # +------------------------------------------+

    def file_save_exists(self):
        if os.path.isfile(self.lyrics_file):
            return True
        return False

    # +-----------------------+
    # | save the lyrics to fs |
    # +-----------------------+

    def file_write(self, lyrics):
        print(self.lyrics_file)
        with open(self.lyrics_file, 'w') as fo:
            fo.write(lyrics)

    def get_lyrics(self, lyrics):
        print('-- new')
        tags = self.cms.tags
        lyrics_text = lyrics.get_lyrics(tags.artist, tags.title)
        main.file_write(lyrics_text)


if __name__ == '__main__':
    cm = CmusPlayer()
    if not cm.is_cmus_playing():
        sys.exit()

    # TODO
    # arguments like:
    # - credential file
    # - retry if NOT FOUND

    try:
        s = Settings()
        s.get_settings()
        lyrics = Lyrics(s.settings)

    except Exception as e:
        sys.exit(e)

    main = Main(cm)

    if (main.cms.is_cmus_playing()):
        main.set_file('/tmp/lyrics/')

        if not main.file_save_exists():
            main.get_lyrics(lyrics)

    main.print_lyrics()
