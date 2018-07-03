import datetime
import json

import flask
import requests

server = flask.Flask(__name__)  # 把这个python文件当做一个web服务


@server.route('/latest1hour', methods=['get', 'post'])  # router里面第一个参数，是接口的路径
def latest1hour():
    today = datetime.datetime.today()
    pre_hour = (today - datetime.timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%SZ')
    url = 'http://192.168.32.11:8983/solr/sentiment/select?q=*:*&fq=country_code:0&fq=timestamp:[%s TO *]&rows=1000&wt=json' % pre_hour
    r = requests.get(url, verify=False)
    r = r.json()['response']['docs']
    return json.dumps(r, ensure_ascii=False)


@server.route('/search', methods=['post'])
def search(request):
    data = request.data
    # url = 'http://192.168.32.11:8983/solr/sentiment/select?q=*:*&fq=country_code:0&fq=timestamp:[%s TO *]&rows=1000&wt=json'
    # r = requests.get(url, verify=False)
    # r = r.json()['response']['docs']
    # return json.dumps(r, ensure_ascii=False)
    return ""


server.run(port=7900, debug=True, host='0.0.0.0')
