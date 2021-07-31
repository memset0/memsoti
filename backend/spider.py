from baiduspider import BaiduSpider

baiduspider = BaiduSpider()


def search(keyword):
    res = []
    for page in range(2):
        rsp = baiduspider.search_web(query=keyword,
                                     exclude=['all'],
                                     pn=page + 1)
        res.extend([result for result in rsp['results'] if result['type'] == 'result'])
    return res
