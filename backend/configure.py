import yaml
from os import path


def load():
    # 配置文件
    file_path = path.join(path.dirname(__file__), '../config.yml')
    with open(file_path, encoding='utf8') as file:
        config = yaml.load(file.read(), Loader=yaml.FullLoader)
        file.close()
    return config
