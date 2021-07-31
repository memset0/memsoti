from os import path
from aip import AipOcr
from pprint import pprint

import configure


class OCR:
    def scan(this, img_path):
        pass

    def filter(this, source):
        if not this.keyword_limit:
            raise Exception('no keyword limit')
        # when all confidence == 1
        return ''.join([x['text'] for x in source])[:this.keyword_limit]


class BaiduOCR(OCR):
    def scan(this, img_path):
        with open(img_path, 'rb') as file:
            img = file.read()
            file.close()
        res = this.client.basicGeneral(img)
        rsp = [{
            'text': it['words'],
            'confidence': 1
        } for it in res['words_result']]
        return rsp

    def __init__(this, app_id, api_key, secret_key):
        this.keyword_limit = 80
        this.app_id = str(app_id)
        this.api_key = str(api_key)
        this.secret_key = str(secret_key)
        this.client = AipOcr(this.app_id, this.api_key, this.secret_key)


if __name__ == '__main__':
    config = configure.load()
    key = config['backend']['baidu_aip']
    ocr = BaiduOCR(key['app_id'], key['api_key'], key['secret_key'])
    dirname = path.abspath(path.dirname(__file__))
    dir = path.join(dirname, '..', config['backend']['upload_folder'], 'p1')
    res = ocr.scan(path.join(dir, 'problem.jpg'))
    pprint(res)
    pprint(ocr.filter(res))
