from baiduspider import BaiduSpider
baiduspider = BaiduSpider()

def search(keyword):
    results = baiduspider.search_web(query=keyword)['results']
    return [result for result in results if result['type'] == 'result']