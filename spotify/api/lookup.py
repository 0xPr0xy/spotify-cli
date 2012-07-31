from spotify.base import Resource
from spotify.connection import ApiTransport
from spotify.models import *


__all__ = ('LookupResource', )


SpotifyLookupModelMap = {
    'album': Album,
    'artist': Artist,
    'track': Track
}


class LookupResource(Resource):

    def __init__(self, api_version=1):
        self.api_version = 1

    def by_id(self, spotify_id):
        response = ApiTransport.get(self._get_url(), uri=spotify_id)
        resource = self.__resource_for_id(spotify_id)
        obj = self._extract_from_response(response.text)
        return resource.from_response(obj)

    def _get_url(self):
        return 'http://ws.spotify.com/lookup/%(version)s/.json' % {
            'version': self.api_version}

    def __resource_for_id(self, spotify_id):
        bits = spotify_id.split(':')
        return SpotifyLookupModelMap[bits[1]]
