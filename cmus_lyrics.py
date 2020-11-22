#!/usr/bin/env python

from cmus_player import CmusPlayer
from settings import Settings
from lyrics import Lyrics
import os
import sys
import subprocess
import argparse


class Main:

    def __init__(self, CmusPlayer):
        self.cms = CmusPlayer
        if (self.cms.is_cmus_playing()):
            self.tags = self.cms.get_tags()

    def print_lyrics(self):
        subprocess.call(["less", self.lyrics_file])

    # +------------------------------------------------------+
    # | set the file path and name removing not alpha chars  |
    # +------------------------------------------------------+

    def set_file(self, path):
        # path + artistname + album
        destintation = os.path.join(path, self.tags.artist, self.tags.album)
        self.create_folders_is_not_exists(destintation)
        # minimize file name

        trackno = str(self.tags.track).zfill(2)
        self.lyrics_file = os.path.join(
            destintation, trackno + ' - ' + self.tags.title + '.txt')
        return self.lyrics_file

    def create_folders_is_not_exists(self, fld):
        if (not os.path.exists(fld) and not os.path.isfile(fld)):
            os.makedirs(fld)

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
        lyrics_text = lyrics.get_lyrics(self.tags.artist, self.tags.title)
        main.file_write(lyrics_text)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--lyricspath', default='/tmp/lyrics',
                        help='Saving Lyrics Path')

    parser.add_argument('-o', '--overwrite',
                        help='Enable search againg',
                        action='store_true')
    args = parser.parse_args()

    print(args.__dict__)
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
        main.set_file(args.lyricspath)

        if not main.file_save_exists() or args.overwrite:
            main.get_lyrics(lyrics)

    main.print_lyrics()
