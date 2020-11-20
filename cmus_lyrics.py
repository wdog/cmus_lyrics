#!/usr/bin/env python

from cmus import CmusPlayer
import lyricsgenius
import os
from collections import namedtuple
import json
import logging
import sys


class Lyrics:

    def __init__(self, CmusPlayer, Genius):
        self.cms = CmusPlayer
        if (self.cms.is_cmus_playing()):
            self.cms.get_tags()

    def get_lyrics(self):
        if (self.cms.is_cmus_playing()):
            self.tags = self.cms.tags
            if self.tags.artist is not None and self.tags.title is not None:
                song = genius.search_song(self.tags.title, self.tags.artist)
                if song is not None:
                    self.lyrics = song.lyrics
                else:
                    self.lyrics = None
        return self.lyrics


class Settings:
    def __init__(self):
        self.get_settings()

    # +----------------------------------------+
    # | Convert Json to Object - hook function |
    # +----------------------------------------+

    def cSecretsDecoder(self, secretsDict):
        return namedtuple('Settings', secretsDict.keys())(*secretsDict.values())

    # +-------------------------------------------+
    # | Get lastFm settings from secret.json file |
    # +-------------------------------------------+

    def get_settings(self):
        try:
            secret_file = "secret.json"
            secret_path = os.path.dirname(os.path.realpath(__file__))

            secret = os.path.join(secret_path, secret_file)
            with open(secret, 'r') as fi:
                self.settings = json.loads(fi.read(),
                                           object_hook=self.cSecretsDecoder)
        except Exception as e:
            logging.critical(str(e))
            sys.exit('no credential')


if __name__ == '__main__':
    cm = CmusPlayer()

    genius = lyricsgenius.Genius(Settings().settings.genius_token)
    cml = Lyrics(cm, genius)
    lyrics = cml.get_lyrics()

    with open("/tmp/cml.txt", "w") as fo:
        fo.write(lyrics)

    os.system("less /tmp/cml.txt")
