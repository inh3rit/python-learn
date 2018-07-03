from elasticsearch import Elasticsearch

es = Elasticsearch('192.168.131.13')
# doc = {
#     'query': {
#         'bool': {
#             'must': [{
#                 'multi_match': {
#                     'query': '周立波',
#                     'fields': ['title', 'content']
#                 }
#             }, {
#                 'range': {
#                     'timestamp': {
#                         'from': '2017-04-10 15:22:41',
#                         'to': '2018-05-14 15:22:41',
#                         'format': 'yyyy-MM-dd HH:mm:ss',
#                         'include_lower': 'true',
#                         'include_upper': 'true'
#                     }
#                 }
#             }, {
#                 'terms': {
#                     'protocol_type': ['HTTP', 'HTTPS', 'FTP', 'SMTP', 'POP3', 'P2P']
#                 }
#             }, {
#                 'terms': {
#                     'resource_type': ['HTML', 'CSS', '图片', '语音', '视频', 'FLASH']
#                 }
#             }]
#         }
#     }
# }
doc = {
    'query': {
        'bool': {
            'must': [{
                'range': {
                    'timestamp': {
                        'gte': '2018-05-15 00:00:00',
                        'lte': '2018-05-16 00:00:00'
                    }
                }
            }]
        }
    }
}
allDoc = es.search(index='tekuan', doc_type='record', body=doc)
sources = map(lambda x: x['_source'], allDoc['hits']['hits'])

print(sources)

# ts = map(lambda x:x+1, range(0,9))
for i, x in enumerate(list(sources)):
    print(i, str(x['title']).__contains__('周立波'), x['title'])
    print(i, str(x['content']).__contains__('周立波'), x['content'])

# for hit in allDoc['hits']['hits']:
#     print hit['_source']
# print(hit['_source']['id'])
