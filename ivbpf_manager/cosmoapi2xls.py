#!/usr/bin/env python
# -*- coding: utf-8 -*-
from CosmoAPIClient import CosmoAPIClient
from xml.etree import ElementTree
import openpyxl as opx
import os


class XnpExcel:
    """
    Export IVBPF (CosmoDB) data to Excel file for excel2xoonips
    """
    def __init__(self):
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

        print(record_fix)

        for i, name in enumerate(record_fix):
            self.ws.cell(column=i+1, row=self.record_index, value=name)

        self.record_index += 1

    def save(self, xls_filename):
        self.wb.save(filename=xls_filename)

if __name__ == '__main__':

    def detail2record(capi, data_id, settings, download_files=True):
        detailxml = capi.get_detail(data_id)

        # print detailxml
        detail_root = ElementTree.fromstring(detailxml.encode('utf-8'))

        # thumbnail
        '''
        thumbnail_path_list = []
        for thumbnail in detail_root[0][6]:
            # print thumbnail.text
            dirname = os.path.join('.', local_img_dir, str(detail_root[0].attrib['data_id']))
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            filename = os.path.join(dirname, thumbnail.text.split('/')[-1])

            if download_thumbnails:
                # FIX: have to refactor
                capi.get_thumbnail(thumbnail.text, filename)
            # FIX: same filename in different dir
            thumbnail_path_list.append(filename)

        thumbnail_path_list = list(set(thumbnail_path_list))
        thumbnail_path = ''
        for path in thumbnail_path_list:
            thumbnail_path += path + '\n'
        '''


        # file/thumbnail
        thumbnail_file = ''
        file_list = []
        for thumbnail in detail_root[0].find('.//thumbnails'):
            dirname = os.path.join('.', settings['local_file_dir'], str(detail_root[0].attrib['data_id']))
            subdirname = thumbnail.text.split('/')[-2]

            if not os.path.isdir(dirname):
                os.makedirs(dirname)

            if subdirname == settings['thumbnail_dir']:
                thumbnail_file = os.path.join(dirname, thumbnail.text.split('/')[-1])
                if download_files:
                    capi.get_file(thumbnail.text, thumbnail_file)

            else:
                if not os.path.isdir(os.path.join(dirname, subdirname)):
                    os.makedirs(os.path.join(dirname, subdirname))

                filename = os.path.join(dirname, subdirname, thumbnail.text.split('/')[-1])
                file_list.append(filename)
                if download_files:
                    capi.get_file(thumbnail.text, filename)

        file_list = list(set(file_list))
        filepath = ''
        for path in file_list:
            filepath += path + '\n'


        # keywords
        keyword_all = ''
        for keyword in detail_root[0].find('.//keyword'):
            keyword_all += keyword.text

        print(filepath)
        # summarize
        record = {'title': detail_root[0].find('.//label').text,
                  'keywords': keyword_all,
                  'description': detail_root[0].find('.//comment').text,
                  'date': detail_root[0].find('.//date').text.replace('-', '/'),
                  'data_type': 'other',
                  'experimenters': detail_root.find('.//author').text,
                  'preview': thumbnail_file.rstrip('\n'),
                  'data_files': filepath,
                  'download_limitation': 'FALSE',
                  'download_notification': 'FALSE',
                  'readme': 'README',
                  'rights': 'CC-BY',
                  'index': '/Public/Data\n/Private/Data' + settings['additional_indexes']
                  }

        print(record)

        return record

    # Setting Templates
    settings_newdb1 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb1',
        'output_filename': 'newdb1.xls',
        'additional_indexes': '\n/Private/BrainAtlas\n/Public/BrainAtlas',
        'local_file_dir': 'tmp',
        'thumbnail_dir': 'img'
    }

    settings_newdb2 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb2',
        'output_filename': 'newdb2.xls',
        'additional_indexes': '\n/Private/Software\n/Public/Software',
        'local_file_dir': 'tmp',
        'thumbnail_dir': 'img'
    }

    # choose settings
    settings = settings_newdb1
    # settings = settings_newdb2

    capi = CosmoAPIClient(settings['url'], settings['db_name'], debug=False)
    listxml = capi.get_list()

    root = ElementTree.fromstring(listxml.encode('utf-8'))

    record_list = []
    thumbnail_list = []

    for child in root[1]:
        record = detail2record(capi, int(child.attrib['data_id']), settings, download_files=True)
        record_list.append(record)

    xnpxls = XnpExcel()

    for record in record_list:
        xnpxls.add_record(record)

    xnpxls.save(settings['output_filename'])
