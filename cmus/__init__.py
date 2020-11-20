#!/usr/bin/env python

import os
import stagger


class CmusPlayer:

    def __init__(self):
        if (self.is_cmus_playing):
            self.get_file_path()

    def get_current(self):
        pass

    def is_cmus_playing(self):
        cmd = "cmus-remote -C status |grep status | awk '{print $2}' "
        r = os.popen(cmd).read().strip()

        if r == 'playing':
            return True
        return False

    def get_file_path(self):
        cmd = "cmus-remote -Q|grep file|awk '{$1=\"\"; print $0}'"
        self.file_path = os.popen(cmd).read().strip()

    def get_album_path(self):
        self.album_path = os.path.dirname(self.file_path)

    def get_tags(self):
        self.tags = stagger.read_tag(self.file_path)


