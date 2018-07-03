import requests
import json

headers = {'Content-Type': 'application/json'}
data = {'key': '周立波', 'timestampstart': '2018-02-14 15:22:41 ', 'timestampend': '2018-05-14 15:22:41 ', 'phone_num': [],
        'protocol_type': ['HTTP', 'HTTPS', 'FTP', 'SMTP', 'POP3', 'P2P'], 'flow_type': '',
        'resource_type': ['HTML', 'CSS', '图片', '语音', '视频', 'FLASH'], 'size': 10, 'from': 0}
r = requests.post('http://192.168.131.16:8102/es/oversearch', headers=headers, data=json.dumps(data))
# r = requests.post('http://localhost:8900/es/oversearch', headers=headers, data=json.dumps(data))
s = r.content.decode('utf8')
result = json.loads(s)

for i, x in enumerate(list(result['searchHit'])):
    print(i, str(x['title']).__contains__('周立波'), x['title'])
    print(i, str(x['content']).__contains__('周立波'), x['content'])
