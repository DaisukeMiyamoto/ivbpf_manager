#!/usr/bin/env python
# -*- coding: utf-8 -*-
from test_cosmoapi import CosmoAPIClient
from xml.etree import ElementTree
# import openpyxl as opx


if __name__ == '__main__':
    url = 'https://invbrain.neuroinf.jp/'
    db_name = 'newdb1'
    capi = CosmoAPIClient(url, db_name, debug=False)
    listxml = capi.get_list()

    root = ElementTree.fromstring(listxml.encode('utf-8'))

    detailxml_all = {}
    for child in root[1]:
        detailxml = capi.get_detail(int(child.attrib['data_id']))
        detailxml_all[child.attrib['data_id']] = detailxml
        print detailxml
