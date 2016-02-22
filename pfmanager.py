# -*- coding: utf-8 -*-
import requests
import time
import BeautifulSoup


class PfManager:
    """
    Data management tool for IVBPF and CNSPF
    """

    PASSWORD_FILE = 'password.txt'
    BASE_URL = 'http://192.168.0.249/xoops/'
    LOGIN_URL = BASE_URL+'user.php'
    REGISTER_URL = BASE_URL+'modules/newdb/register.php'
    DETAIL_URL = BASE_URL+'modules/newdb/detail.php'
    DELETE_URL = BASE_URL+'modules/newdb/config.php'

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
            'dir': 'mor',
            'caption': thumbname,
            'uploaded_data': uploaded_data,
            'kw[]': keywords,
            'method': 'do_reg'
        }
        print 'thumbpath: '+thumbpath
        thumbpath = u'100303_3.f.snapshot.jpg'
        files = {
            'thumbfile': (thumbname, open(thumbpath, 'rb'), 'image/png'),
        }
        r = self.session.post(self.REGISTER_URL, data=data, files=files)

        if r.status_code != 200:
            print 'Error: add failed.'
            return

        if self.show_result:
            print r.text

    def get_record(self, id):
        data = {
            'name': '',
            'comment': 'BoND ID: '+str(id)+'<br />',
            'thumbname': '',
            'thumbpath': '',
        }
        r = self.session.get(self.DETAIL_URL+'?id='+str(id))

        if self.show_result:
            print r.text

        soup = BeautifulSoup.BeautifulSoup(r.text)

        text = soup.find(id='data_name').string
        if text is not None:
            data['name'] = text.strip()

        text = soup.find('img').string
        print text
        if text is not None:
            data['comment'] += text.strip()

        for record in soup.findAll('img'):
            if 'extract' in record.get('src'):
                filename = record.get('src').split('/')[-1]
                if data['thumbpath'] == '':
                    data['thumbname'] = filename
                    data['thumbpath'] = filename

                with open('./'+filename, 'wb') as f:
                    raw = self.session.get(record.get('src')).content
                    f.write(raw)

        return data

    def del_record(self, id):
        data = {
            'lid': id,
            'mode': 'do_ddel'
        }
        r = self.session.post(self.DELETE_URL, data=data)
        if self.show_result:
            print r.text

    def get_keywordtree(self):
        pass

    def make_archive(self, name, filepath):
        pass
        # archive = zipfile.ZipFile('./'.name+'.tar.gz', 'w', filepath, zipfile.ZIP_DEFLATED)
        # archive.write('')

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

    # for i in range(1425, 1430):
    #     pfm.del_record(i)

    data = pfm.get_record('1384')
    #pfm.get_record('932')

    #pfm.add_record(**example)
    print data
    data['uploaded_data'] = u'030504_1_sn/model'
    pfm.add_record(**data)

