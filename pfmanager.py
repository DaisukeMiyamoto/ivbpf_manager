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

    def __init__(self, base_url='http://192.168.0.249/xoops/', db_name='newdb'):
        self.base_url = base_url
        self.db_name = db_name+'/'
        self.login_info = {'uname': 'automoth',
                           'pass': '******',
                           'op': 'login'
                           }
        self.session = None
        self.show_result = False

        passfile = open(self.PASSWORD_FILE, 'r')
        self.login_info['pass'] = passfile.read()
        self._login()


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
        files = {
            'thumbfile': (thumbname, open(thumbpath, 'rb'), 'image/png'),
        }
        r = self.session.post(self.base_url + 'modules/' + self.db_name + self.REGISTER_URL, data=data, files=files)

        if r.status_code != 200:
            print 'Error: add failed.'
            return

        print r.text
        if self.show_result:
            print r.text

    def get_record(self, id):
        data = {
            'name': '',
            'comment': 'BoND ID: '+str(id)+'\n',
            'thumbname': '',
            'thumbpath': '',
            'keywords': []
        }
        r = self.session.get(self.base_url + 'modules/' + self.db_name + self.DETAIL_URL+'?id='+str(id))

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
            print text
            data['comment'] += text.strip()

        # get keywords
        for record in soup.findAll('span'):
            for attrs in record.attrs:
                if attrs[0] == 'keyword_id':
                    print attrs[1]
                    data['keywords'].append(str(attrs[1]))
                    

        # get thumbnail image
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
        r = self.session.post(self.base_url + 'modules/' + self.db_name + self.DELETE_URL, data=data)
        if self.show_result:
            print r.text

    def get_keywordtree(self):
        pass

    def make_archive(self, name, filepath):
        pass
        # archive = zipfile.ZipFile('./'.name+'.tar.gz', 'w', filepath, zipfile.ZIP_DEFLATED)
        # archive.write('')

if __name__ == '__main__':

    def exec_by_file(pfm, ivbpfm):
        filename = '/home/nebula/work/ivbpf/uploadtable20160108.txt'
        reader = csv.reader(open(filename))

        for record in reader:
            data = pfm.get_record(str(record[0]))
            #print data
            data['uploaded_data'] = u''
            data['keywords'] = {'134'}
            
            #pfm.add_record(**data)
            print 'Register: ' + data['name'] + '(' + record[0] + ')'
            ivbpfm.add_record(**data)

    def exec_one_record(pfm, ivbpfm, dbid):
            data = pfm.get_record(dbid)
            #ivbpfm.add_record(**data)




    pfm = PfManager()
    ivbpfm = PfManager(base_url='https://invbrain.neuroinf.jp/html_test/', db_name='newdb5')

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

    # for i in range(1425, 1430):
    #     pfm.del_record(i)

    dbid = '1384'

    exec_one_record(pfm, ivbpfm, dbid)




