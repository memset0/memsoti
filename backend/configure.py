import os
import yaml

def load():
	# 配置文件
	with open(os.path.join(os.path.dirname(__file__), '../config.yml'), encoding='utf8') as file:
		config = yaml.load(file.read(), Loader=yaml.FullLoader)
		file.close()
	return config