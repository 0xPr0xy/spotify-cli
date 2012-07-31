from spotify.base import Resource
from spotify.connection import ApiTransport


__all__ = ('SearchResource', )


class SearchResource(Resource):

    def __init__(self, resource, api_version=1):
        self.resource = resource
        self.api_version = api_version

    def search(self, query):
        response = ApiTransport.get(self._get_url(), q=query)
        results = self._extract_from_response(response.text)

        for obj in results:
            yield self.resource.from_response(obj)

    def _get_wrapper_key(self, data):
        return self.resource.wrapper

    def _get_url(self):
        return 'http://ws.spotify.com/search/%(version)s/%(resource)s.json' % {
            'version': self.api_version,
            'resource': self.resource.resource_name}
