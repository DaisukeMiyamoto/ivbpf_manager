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


        # label
        title = detail_root[0].find('.//label').text
        if title is None or title == ' ---':
            title = settings['db_title'] + str(detail_root[0].attrib['data_id'])

        # description
        description = ''
        if detail_root[0].find('.//comment') is not None and detail_root[0].find('.//comment').text is not None:
            description = detail_root[0].find('.//comment').text.rstrip()

        # file/thumbnail
        thumbnail_file = u''
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
        if len(file_list) == 0:
            filepath = 'dummy.txt'
        else:
            filepath = file_list[0]


        # experimenters
        experimenters = detail_root.find('.//author').text
        if experimenters is None:
            experimenters = 'no data'


        # keywords
        keyword_list = []
        keyword_all = ''
        for metadata in detail_root[0].findall('.//component'):
            if metadata.text is not None and metadata.text != '':
                keyword_list.append(metadata.attrib['name'] + ': ' + metadata.text.replace('\n', ''))

        for keyword in detail_root[0].find('.//keywords'):
            keyword_list.append(keyword.text)

        keyword_list = list(set(keyword_list))
        for keyword in keyword_list:
            keyword_all += keyword + '\n'



        # indexes
        index_list = []
        indexes = ''
        index_list.append(settings['db_title'])
        for keyword in detail_root[0].find('.//keywords'):
            keyword_sep = keyword.text.split('/')
            for i in range(1, len(keyword_sep)):
                joined = ''.join(keyword_sep[0:i])
                index_list.append(settings['db_title'] + '/Keyword/' + joined)

            index_list.append(settings['db_title'] + '/Keyword/' + keyword.text)

        index_list = list(set(index_list))

        for index in index_list:
            indexes += '/Private/'+index+'\n' + '/Public/'+index+'\n'





        # summarize
        record = {'title': title,
                  'keywords': keyword_all.rstrip('\n'),
                  'description': description,
                  'date': detail_root[0].find('.//date').text.replace('-', '/'),
                  'data_type': 'other',
                  'experimenters': experimenters,
                  'preview': thumbnail_file.replace('\\', '/').rstrip('\n'),
                  'data_files': filepath.replace('\\', '/').rstrip('\n'),
                  'download_limitation': 'FALSE',
                  'download_notification': 'FALSE',
                  'readme': 'README',
                  'rights': 'CC-BY',
                  'index': (indexes + settings['additional_indexes']).rstrip('\n')
                  }


        print(record)

        return record

    # Setting Templates
    settings_newdb1 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb1',
        'db_title': 'Brain Garalley',
        'output_filename': 'newdb1.xlsx',
        'additional_indexes': '',
        'local_file_dir': 'newdb1',
        'thumbnail_dir': 'img',
    }

    settings_newdb2 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb2',
        'db_title': 'Software',
        'output_filename': 'newdb2.xlsx',
        'additional_indexes': '',
        'local_file_dir': 'newdb2',
        'thumbnail_dir': 'img',
    }

    settings_newdb5 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb5',
        'db_title': 'Brain and Neurons/Silkmoth',
        'output_filename': 'newdb5.xlsx',
        'additional_indexes': '',
        'local_file_dir': 'newdb5',
        'thumbnail_dir': 'mor',
    }
    settings_newdb10 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb10',
        'db_title': 'Sensory System',
        'output_filename': 'newdb10.xlsx',
        'additional_indexes': '',
        'local_file_dir': 'newdb10',
        'thumbnail_dir': 'img',
    }

    settings_newdb112 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb112',
        'db_title': 'Brain and Neurons/Honeybee',
        'output_filename': 'newdb112.xlsx',
        'additional_indexes': '',
        'local_file_dir': 'newdb112',
        'thumbnail_dir': 'img',
    }

    settings_newdb9 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb9',
        'db_title': 'Brain and Neurons/Cricket',
        'output_filename': 'newdb9.xlsx',
        'additional_indexes': '',
        'local_file_dir': 'newdb9',
        'thumbnail_dir': 'img',
    }

    settings_newdb12 = {
        'url': 'https://invbrain.neuroinf.jp/',
        'db_name': 'newdb12',
        'db_title': 'Brain and Neurons/Fly',
        'output_filename': 'newdb12.xlsx',
        'additional_indexes': '',
        'local_file_dir': 'newdb12',
        'thumbnail_dir': 'img',
    }

    # choose settings
    settings = settings_newdb10
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
