#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from xml.etree import ElementTree


class CosmoAPIClient:

    USERNAME = 'automoth'
    PASSWORD_FILE = 'password.txt'
    MODULE_URI = 'modules/cosmoapi/index.php/'

    LOGIN = 'login?uname=%s&pass=%s'
    LIST = 'list/%s'
    SEARCH_KEYWORD = 'search/%s'
    GET = 'get/%s/%d'  # module name, data id

    def __init__(self, base_url, db_name, debug=False):
        self.base_url = base_url
        self.db_name = db_name
        self.debug = debug
        passfile = open(self.PASSWORD_FILE, 'r')
        password = passfile.read()

        self._login(password)

    def _login(self, password):
        self.session = requests.Session()
        login_uri = self.base_url + self.MODULE_URI + (self.LOGIN % ('automoth', password))
        if self.debug:
            print(login_uri)
        r = self.session.post(login_uri)

        if self.debug:
            print(r.text)

    def get_list(self):
        list_uri = self.base_url + self.MODULE_URI + (self.LIST % self.db_name)
        if self.debug:
            print(list_uri)
        r = self.session.get(list_uri)
        if self.debug:
            print(r.text)

        return r.text

    def get_detail(self, data_id):
        get_uri = self.base_url + self.MODULE_URI + (self.GET % (self.db_name, data_id))

        r = self.session.get(get_uri)
        if self.debug:
            print(r.text)

        return r.text

    def get_thumbnail(self, uri, filename):
        # print(uri + ': ' + urllib.parse.urlencode(uri))
        with open(filename, 'wb') as f:
            raw = self.session.get(uri.replace('%', '%25')).content
            f.write(raw)

    def get_file(self, uri, filename):
        self.get_thumbnail(uri, filename)


if __name__ == '__main__':
    url = 'https://invbrain.neuroinf.jp/'
    db_name = 'newdb1'
    capi = CosmoAPIClient(url, db_name, debug=False)
    listtext = capi.get_list()

    root = ElementTree.fromstring(listtext.encode('utf-8'))

    for child in root[1]:
        print(child.tag, child.attrib)

    detailtext = capi.get_detail(59)
    print(detailtext)
