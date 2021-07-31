import cv2
import numpy as np
from os import path
from math import sqrt

import configure


def _dis(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return sqrt(dx * dx + dy * dy)


def transform(source, target, vec2=[], size=1000):
    img = cv2.imread(source)
    if len(vec2) == 0:
        w, h = img.shape[:2]
        vec2 = [[0, 0], [w, 0], [0, h], [w, h]]
    k = sqrt(_dis(vec2[0], vec2[2]) * _dis(vec2[1], vec2[3]) / _dis(vec2[0], vec2[1]) / _dis(vec2[2], vec2[3])) # h / w
    if k < 1:
        w, h = size, max(1, round(k * size))
    else:
        w, h = max(1, round(size / k)), size
    V0 = np.float32(vec2)
    V1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    M = cv2.getPerspectiveTransform(V0, V1)
    result = cv2.warpPerspective(img, M, (w, h))
    cv2.imwrite(target, result)


if __name__ == '__main__':
    config = configure.load()
    dir = path.abspath(path.join(path.dirname(__file__), '..', config['backend']['upload_folder'], 'p1'))
    transform(path.join(dir, 'source.jpg'), path.join(dir, 'problem.jpg'), [[649, 1771], [3569, 1601], [584, 2570], [3685, 2379]])