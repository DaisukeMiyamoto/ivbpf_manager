# -*- coding: utf-8 -*-

import requests


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
        self.login()

    def login(self):
        self.session = requests.Session()
        self.session.headers.update({'referer': self.REGISTER_URL})
        print self.login_info
        r = self.session.post(self.LOGIN_URL, data=self.login_info)

        if self.show_result:
            print r.text

    def add_record(self, title, comment='', thumbname=''):
        reg_data = {
            'name': title,
            'comment': comment,
            'dir': 'img',
            'method': 'do_reg'
        }
        r = self.session.post(self.REGISTER_URL, data=reg_data)

        if self.show_result:
            print r.text


if __name__ == '__main__':
    pfm = PfManager()
    pfm.add_record('test6', 'comment6')



