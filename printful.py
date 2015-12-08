"""
printful
~~~~~~~~

This module interacts with the Printful API

"""

import requests
import json
from urllib.parse import urljoin
from base64 import standard_b64encode
from functools import partialmethod


class PrintfulException(Exception):
    """ Used for response JSON validation """


class PrintfulAPIException(Exception):
    """ Invalid API Server Responses
    """
    def __init__(self, resp):
        self.code = resp['code']
        self.result = resp['result']

    def __str__(self):
        return 'Server Response {0}: {1}'.format(self.code,
                                          self.result)


class Printful:

    def __init__(self, key):
        """
        This is the main client that handles all of the requests
        to the Printful API.  The class uses [requests](http://docs.python-requests.org/en/latest/)
        as a way to interact with the server.

        :param key:

        Usage::

            >>> import printful
            >>> pf = printful.Printful(key)
            >>> orders = pf.get('orders')

        """
        self.key = bytearray(key, 'utf-8')
        self.api_url = 'https://api.theprintful.com/'
        self.user_agent = 'Printful API Python Library 1.2'
        self._response = {}

    @property
    def request_headers(self):
        return {'Authorization': 'Basic {0}'.format(self._auth()),
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json'}

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, val):
        try:
            resp = self._to_dict(val)
        except ValueError:
            raise PrintfulException('API response was not valid JSON.')
        self._response = resp

    def _request(self, method, path, **params):
        params.update(verify=True, headers=self.request_headers)
        url = urljoin(self.api_url, path)
        r = requests.request(method, url, **params)
        if r.status_code not in range(200, 301):
            raise PrintfulAPIException(self._to_dict(r.json()))
        self.response = r.json()
        return self.response

    def _auth(self):
        return standard_b64encode(self.key).decode('ascii')

    def _http_method(self, method, path, **params):
        return self._request(method, path, **params)

    def _to_dict(self, json_obj):
        return json.loads(json.dumps(json_obj))

    get = partialmethod(_http_method, 'GET')
    post = partialmethod(_http_method, 'POST')
    put = partialmethod(_http_method, 'PUT')
    delete = partialmethod(_http_method, 'DELETE')


    def item_count(self):
        """
        Get the number of items returned in the last response.
        Helpful for result sets that may require paginated requests.
        :return: int

        """
        if self.response:
            try:
                return self.response['paging'].get('total', None)
            except KeyError:
                raise PrintfulException('API response did not contain paginated results.')
        return None







