# -*- coding: utf-8 -*-
import requests
import BeautifulSoup
import csv


class PfManager:
    """
    Data management tool for IVBPF and CNSPF
    """

    PASSWORD_FILE = 'password.txt'
    LOGIN_URL = 'user.php'
    REGISTER_URL = 'register.php'
    DETAIL_URL = 'detail.php'
    DELETE_URL = 'config.php'

    def __init__(self, base_url='http://192.168.0.249/xoops/', db_name='newdb', keyword_table_file=''):
        self.base_url = base_url
        self.db_name = db_name + '/'
        self.login_info = {'uname': 'automoth',
                           'pass': '******',
                           'op': 'login'
                           }
        self.session = None
        self.show_result = False
        self.keyword_table = {}

        passfile = open(self.PASSWORD_FILE, 'r')
        self.login_info['pass'] = passfile.read()
        self._login()

        if keyword_table_file != '':
            reader = csv.reader(open(keyword_table_file))
            for record in reader:
                self.keyword_table[record[0]] = {'name': record[1], 'converted': record[2]}

    def _login(self):
        self.session = requests.Session()
        self.session.headers.update({'referer': self.base_url + 'modules/' + self.db_name + self.REGISTER_URL})
        r = self.session.post(self.base_url + self.LOGIN_URL, data=self.login_info)

        if self.show_result:
            print r.text

    def add_record(self, name, comment='', thumbname='', thumbpath='', uploaded_data='', keywords=''):
        data = {
            'name': name,
            'comment': comment,
            'dir': 'mor',
            'caption': thumbname,
            'uploaded_data': uploaded_data,
            'kw[]': keywords,
            'method': 'do_reg'
        }
        print(data)
        files = {
            'thumbfile': (thumbname, open(thumbpath, 'rb'), 'image/png'),
        }
        r = self.session.post(self.base_url + 'modules/' + self.db_name + self.REGISTER_URL, data=data, files=files)

        if r.status_code != 200:
            print 'Error: add failed.'
            return

        soup = BeautifulSoup.BeautifulSoup(r.text)
        print(soup.find('h4').text.strip())

        if self.show_result:
            print r.text

    def get_record(self, id):
        data = {
            'name': '',
            'comment': 'BoND_ID(' + str(id) + ')\n',
            'thumbname': '',
            'thumbpath': '',
            'keywords': []
        }
        r = self.session.get(self.base_url + 'modules/' + self.db_name + self.DETAIL_URL + '?id=' + str(id))

        if self.show_result:
            print r.text

        soup = BeautifulSoup.BeautifulSoup(r.text)

        # get data name
        text = soup.find(id='data_name').string
        if text is not None:
            data['name'] = text.strip()

        # get comment
        text = soup.find(id='data_comment').text
        if text is not None:
            data['comment'] += text.strip()

        # get keywords
        for record in soup.findAll('span'):
            for attrs in record.attrs:
                if attrs[0] == 'keyword_id':
                    data['keywords'].append(str(attrs[1]))

        # get thumbnail image
        for record in soup.findAll('img'):
            if 'extract' in record.get('src'):
                filename = record.get('src').split('/')[-1]
                if data['thumbpath'] == '':
                    data['thumbname'] = filename
                    data['thumbpath'] = filename

                with open('./' + filename, 'wb') as f:
                    raw = self.session.get(record.get('src')).content
                    f.write(raw)

        return data

    def del_record(self, id):
        data = {
            'lid': id,
            'mode': 'do_ddel'
        }
        r = self.session.post(self.base_url + 'modules/' + self.db_name + self.DELETE_URL, data=data)
        if self.show_result:
            print r.text

    def get_keywordtree(self):
        pass

    def make_archive(self, name, filepath):
        pass
        # archive = zipfile.ZipFile('./'.name+'.tar.gz', 'w', filepath, zipfile.ZIP_DEFLATED)
        # archive.write('')

    def convert_keyword(self, keywords):
        ret = []
        for key in keywords:
            if self.keyword_table[key]['converted'] != '0':
                ret.append(self.keyword_table[key]['converted'])

        return ret


if __name__ == '__main__':

    def exec_by_file(pfm, ivbpfm, filename):
        reader = csv.reader(open(filename))

        for record in reader:
            exec_one_record(pfm, ivbpfm, record[0])


    def exec_one_record(pfm, ivbpfm, dbid):
        data = pfm.get_record(dbid)
        data['keywords'] = ivbpfm.convert_keyword(data['keywords'])
        data['uploaded_data'] = dbid + '/data/'
        ivbpfm.add_record(**data)


    pfm = PfManager()
    ivbpfm = PfManager(base_url='https://invbrain.neuroinf.jp/', db_name='newdb5',
                       keyword_table_file='/home/nebula/work/ivbpf/table.csv')

    '''
    example = {
        'name': '040823_3_sn',
        'comment': time.strftime('%X %x'),
        'thumbname': '040823_3_sn.jpg',
        'thumbpath': './data_example/040823_3_sn/img/040823_3_sn.jpg',
        'uploaded_data': '030504_1_sn',
        'keywords': {'5', '6'}
    }
    '''

    # for i in range(574, 730):
    #    ivbpfm.del_record(i)

    # dbid = '1355'
    # exec_one_record(pfm, ivbpfm, dbid)

    filename = '/home/nebula/work/ivbpf/upload20160224_2.txt'
    exec_by_file(pfm, ivbpfm, filename)
