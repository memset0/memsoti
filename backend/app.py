import os
import flask
import shutil
import random
from os import path
from pprint import pprint
from flask import Flask, request

import image
import spider
import configure
from ocr import BaiduOCR

dirname = path.dirname(__file__)

# 配置文件
full_config = configure.load()
config = full_config['backend']
MODE = full_config['mode']

# 数据
data = config['test_data'] if 'test_data' in config else {}

# Flask App
app = Flask(__name__)
app.config['mode'] = MODE

# OCR
ocr = BaiduOCR(config['baidu_aip']['app_id'],
               config['baidu_aip']['api_key'],
               config['baidu_aip']['secret_key'])

# 临时文件上传目录
upload_folder = path.abspath(path.join(dirname, '..', config['upload_folder']))
app.config['upload_folder'] = upload_folder
if path.exists(upload_folder) and MODE != 'development':
    shutil.rmtree(upload_folder)
if not path.exists(upload_folder):
    os.mkdir(upload_folder)


# 图片处理
def handleImage(id, cutter=[]):
    dir = path.join(app.config['upload_folder'], id)
    image.transform(path.join(dir, 'source.jpg'),
                    path.join(dir, 'problem.jpg'),
                    vec2=cutter)
    text = ocr.scan(path.join(dir, 'problem.jpg'))
    return {'text': text, 'type': 'image'}


# 上传图片
@app.route('/upload/image', methods=['POST'])
def uploadImage():
    file = request.files['file']
    id = random.sample(config['id_charset'], 8)
    dist_dir = path.join(app.config['upload_folder'], id)
    os.mkdir(dist_dir)
    file.save(path.join(dist_dir, 'source.jpg'))
    data[id] = handleImage(dist_dir)
    return flask.jsonify({'code': 200, 'id': id, 'data': data[id]})


# 查看图片
@app.route('/view/image/<id>', methods=['GET'])
def viewImage(id):
    target_dir = path.join(app.config['upload_folder'], id)
    if id not in data:
        return flask.abort(404)
    with open(path.join(target_dir, 'problem.jpg'), 'rb') as file:
        image = file.read()
        response = flask.Response(image, mimetype='image/jpg')
        file.close()
    return response


# 搜索结果
@app.route('/search/<id>', methods=['GET'])
def search(id):
    if id not in data:
        return flask.abort(404)
    if 'result' not in data[id]:
        data[id]['result'] = spider.search(data[id]['text'])
    return flask.jsonify(data[id]['result'])


if __name__ == '__main__':
    if MODE == 'development':
        for id in config['test_data']:
            it = config['test_data'][id]
            if it['type'] == 'image' and 'text' not in it:
                cutter = it['cutter'] if 'cutter' in it else []
                data[id] = handleImage(id, cutter)
        pprint(data)
    app.run(host='0.0.0.0', port=config['port'], debug=(MODE == 'development'))
