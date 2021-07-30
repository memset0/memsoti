import os
import yaml
import flask
import shutil
import random

import spider

dirname = os.path.dirname(__file__)

app = flask.Flask(__name__)

# 配置文件
with open(os.path.join(dirname, '../config.yml'), encoding='utf8') as file:
	config = yaml.load(file.read(), Loader=yaml.FullLoader)
	file.close()

# 数据
data = config['backend']['test_data'] if 'test_data' in config['backend'] else {}

# 临时文件上传目录
upload_folder = os.path.abspath(os.path.join(dirname, '..', config['backend']['upload_folder']))
app.config['upload_folder'] = upload_folder
if os.path.exists(upload_folder) and config['mode'] != 'development':
	shutil.rmtree(upload_folder)
if not os.path.exists(upload_folder):
	os.mkdir(upload_folder)

# 上传图片
@app.route('/upload/image', methods=['POST'])
def uploadImage():
	file = flask.request.files['file']
	id = random.sample(config['id_charset'], 8)
	dist_dir = os.path.join(app.config['upload_folder'], id)
	os.mkdir(dist_dir)
	file.save(os.path.join(dist_dir, 'source.jpg'))
	text = '' # TODO: 图片处理 / OCR
	file.save(os.path.join(dist_dir, 'problem.jpg'))
	data[id] = {'text': text, 'type': 'image'}
	return flask.jsonify({'code': 200, 'id': id, 'data': data[id]})

# 查看图片
@app.route('/view/image/<id>', methods=['GET'])
def viewImage(id):
	target_dir = os.path.join(app.config['upload_folder'], id)
	if not id in data:
		return flask.abort(404)
	with open(os.path.join(target_dir, 'problem.jpg'), 'rb') as file:
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