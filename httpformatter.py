from urllib import parse, request


class HttpFormatter:
    def __init__(self, domain):
        self.domain = domain

    def request(self, dic):
        url = self.domain + 'Buscador?'

        data = parse.urlencode(dic).encode("utf-8")
        content = request.urlopen(url + data.decode())

        return content.read()

    def get(self, querystring):
        url = self.domain + querystring

        content = request.urlopen(url)

        return content.read()
