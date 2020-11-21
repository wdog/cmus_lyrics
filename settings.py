#!/usr/bin/env python

from collections import namedtuple
import json
import os


class Settings:
    def __init__(self, secrets='secret.json'):
        self.secrets = secrets

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
            # get path of the credential file
            secret_path = os.path.dirname(os.path.realpath(__file__))

            secret_file = os.path.join(secret_path, self.secrets)

            self.settings = json.load(open(secret_file))

        except Exception as e:
            raise CredentialsError(e)


class CredentialsError(Exception):
    """ no credentials file found """
    pass
