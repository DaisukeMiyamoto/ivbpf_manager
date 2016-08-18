#!/usr/bin/env python
# -*- coding: utf-8 -*-
from test_cosmoapi import CosmoAPIClient
from xml.etree import ElementTree
import openpyxl as opx
import os


class XnpExcel:
    def __init__(self, xls_filename):
        self.wb = opx.Workbook()
        self.ws = self.wb.active
        self.ws.title = 'data'

        self.write_header()
        self.record_index = 2

    def write_header(self):
        header = ['ID',
                  '言語',
                  'タイトル',
                  'フリーキーワード',
                  '概要',
                  '日付',
                  'データタイプ',
                  '実験者',
                  'プレビューファイルパス',
                  'データファイルパス',
                  'ダウンロード制限',
                  'ダウンロード通知',
                  'README',
                  'Rights',
                  'インデックス'
                  ]
        for i, name in enumerate(header):
            self.ws.cell(column=i+1, row=1, value=name)

    def add_record(self, record):
        item_list = ['doi',
                     'langs',
                     'title',
                     'keywords',
                     'description',
                     'date',
                     'data_type',
                     'experimenters',
                     'preview',
                     'data_files',
                     'download_limitation',
                     'download_notification',
                     'readme',
                     'rights',
                     'index'
                     ]

        record_fix = []
        for item in item_list:
            if item in record:
                record_fix.append(record[item])
            else:
                record_fix.append('')

        print record_fix

        for i, name in enumerate(record_fix):
            self.ws.cell(column=i+1, row=self.record_index, value=name)

        self.record_index += 1

    def save(self):
        self.wb.save(filename=xls_filename)

if __name__ == '__main__':
    url = 'https://invbrain.neuroinf.jp/'
    db_name = 'newdb1'
    local_img_dir = 'img'
    capi = CosmoAPIClient(url, db_name, debug=False)
    listxml = capi.get_list()

    root = ElementTree.fromstring(listxml.encode('utf-8'))

    record_list = []
    detailxml_all = {}
    thumbnail_list = []

    for child in root[1]:
        detailxml = capi.get_detail(int(child.attrib['data_id']))
        detailxml_all[child.attrib['data_id']] = detailxml

        print detailxml
        detail_root = ElementTree.fromstring(detailxml.encode('utf-8'))

        print detail_root[0][0].text

        thumbnail_path_list = []
        for thumbnail in detail_root[0][6]:
            print thumbnail.text
            dirname = os.path.join('.', local_img_dir, str(detail_root[0].attrib['data_id']))
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            filename = os.path.join(dirname, thumbnail.text.split('/')[-1])
            # FIX: same filename in different dir
            thumbnail_path_list.append(filename)

        thumbnail_path_list = list(set(thumbnail_path_list))
        thumbnail_path = ''
        for path in thumbnail_path_list:
            thumbnail_path += path + '\n'

        record = {'title': detail_root[0][0].text,
                  'date': detail_root[0][2].text.replace('-', '/'),
                  'data_type': 'other',
                  'experimenters': detail_root[0][1].text,
                  'preview': thumbnail_path.rstrip('\n'),
                  'data_files': 'dummy.txt',
                  'download_limitation': 'FALSE',
                  'download_notification': 'FALSE',
                  'readme': 'README',
                  'rights': 'CC-BY',
                  'index': '/Public/Data\n/Private/Data\n/Private/BrainAtlas'
                  }

        record_list.append(record)

    xls_filename = 'test.xls'

    xnpxls = XnpExcel(xls_filename)

    for record in record_list:
        xnpxls.add_record(record)

    xnpxls.save()