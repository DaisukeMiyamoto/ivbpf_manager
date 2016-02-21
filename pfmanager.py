# -*- coding: utf-8 -*-
import requests
import time


class PfManager:
    """
    Data management tool for IVBPF and CNSPF
    """

    PASSWORD_FILE = 'password.txt'
    BASE_URL = 'http://192.168.0.249/xoops/'
    LOGIN_URL = BASE_URL+'user.php'
    REGISTER_URL = BASE_URL+'modules/newdb/register.php'

    def __init__(self):
        self.login_info = {'uname': 'automoth',
                           'pass': '******',
                           'op': 'login'
                           }
        self.session = None
        self.show_result = True

        passfile = open(self.PASSWORD_FILE, 'r')
        self.login_info['pass'] = passfile.read()
        self._login()

    def _login(self):
        self.session = requests.Session()
        self.session.headers.update({'referer': self.REGISTER_URL})
        print self.login_info
        r = self.session.post(self.LOGIN_URL, data=self.login_info)

        if self.show_result:
            print r.text

    def add_record(self, name, comment='', thumbname='', thumbpath='', uploaded_data='', keywords=''):
        data = {
            'name': name,
            'comment': comment,
            'dir': 'img',
            'caption': thumbname,
            'uploaded_data': uploaded_data,
            'kw[]': keywords,
            'method': 'do_reg'
        }
        files = {
            'thumbfile': (thumbname, open(thumbpath, 'rb'), 'image/png'),
        }
        r = self.session.post(self.REGISTER_URL, data=data, files=files)
        print r.headers

        if r.status_code != 200:
            print 'Error: add failed.'
            return

        if self.show_result:
            print r.text

    def get_keywordtree(self):
        pass

if __name__ == '__main__':
    pfm = PfManager()
    example = {
        'name': '040823_3_sn',
        'comment': time.strftime('%X %x'),
        'thumbname': '040823_3_sn.jpg',
        'thumbpath': './data_example/040823_3_sn/img/040823_3_sn.jpg',
        'uploaded_data': '030504_1_sn',
        'keywords': {'5', '6'}
    }
    pfm.add_record(**example)
