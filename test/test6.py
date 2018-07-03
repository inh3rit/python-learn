import requests

headers = {
    'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8'.encode('utf-8').decode('latin1'),
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Connection': 'keep-alive',
    'Cookie': 'SMYUV=1522055806000545; IPLOC=…ID=rvuscdu1kmm8a96lg6jinsbrq4'.encode('utf-8').decode('latin1'),
    'Host': 'www.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/60.0'.encode('utf-8').decode('latin1')
}
response = requests.get('http://www.sogou.com/labs/sogoudownload/SogouCA/news_tensite_xml.full.tar.gz'
                        , auth=('391552129@qq.com', 'EOg^I{WmTDLycP4^')
                        , headers=headers)
print(response)
