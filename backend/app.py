import os
import flask
import shutil
import random
from os import path

import image
import spider
import configure

dirname = path.dirname(__file__)

app = flask.Flask(__name__)
config = configure.load()

# 数据
data = config['backend']['test_data'] if 'test_data' in config['backend'] else {}

# 临时文件上传目录
upload_folder = path.abspath(path.join(dirname, '..', config['backend']['upload_folder']))
app.config['upload_folder'] = upload_folder
if path.exists(upload_folder) and config['mode'] != 'development':
	shutil.rmtree(upload_folder)
if not path.exists(upload_folder):
	os.mkdir(upload_folder)

# 上传图片
@app.route('/upload/image', methods=['POST'])
def uploadImage():
	file = flask.request.files['file']
	id = random.sample(config['id_charset'], 8)
	dist_dir = path.join(app.config['upload_folder'], id)
	os.mkdir(dist_dir)
	file.save(path.join(dist_dir, 'source.jpg'))
	image.transform(path.join(dist_dir, 'source.jpg'), path.join(dist_dir, 'problem.jpg'))
	text = '' # TODO: 图片处理 / OCR
	data[id] = {'text': text, 'type': 'image'}
	return flask.jsonify({'code': 200, 'id': id, 'data': data[id]})

# 查看图片
@app.route('/view/image/<id>', methods=['GET'])
def viewImage(id):
	target_dir = path.join(app.config['upload_folder'], id)
	if not id in data:
		return flask.abort(404)
	with open(path.join(target_dir, 'problem.jpg'), 'rb') as file:
		image = file.read()
		response = flask.Response(image, mimetype='image/jpg')
		file.close()
	return response

# 搜索结果
@app.route('/search/<id>', methods=['GET'])
def search(id):
	if not id in data:
		return flask.abort(404)
	if not 'result' in data[id]:
		data[id]['result'] = spider.search(data[id]['text'])
	return flask.jsonify(data[id]['result'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config['backend']['port'], debug=(config['mode'] == 'development'))