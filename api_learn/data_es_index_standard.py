import datetime
import sys
import pymysql.cursors
from elasticsearch import Elasticsearch
import elasticsearch.helpers as helpers
import threading
import requests
import json
import random

# 协议类型
protocol_dict = {'HTTP': 8, 'HTTPS': 6, 'FTP': 1, 'SMTP': 2, 'POP3': 2, 'P2P': 1}
protocol_list = []
# 流量类型
flow_list = ['上行', '下行']
# 资源类型
resource_dict = {'HTML': 32, 'CSS': 3, '图片': 2, '语音': 1, '视频': 1, 'FLASH': 1}
resource_list = []

user_data_count = {}


def random_protocol_by_weight():
    global protocol_list
    if protocol_list.__len__() == 0:
        for k, v in protocol_dict.items():
            protocol_list += [k] * v
    return random.choice(protocol_list)


def random_resource_by_weight():
    global resource_list
    if resource_list.__len__() == 0:
        for k, v in resource_dict.items():
            resource_list += [k] * v
    return random.choice(resource_list)


def get_user_info():
    result = None
    # 连接MySQL数据库
    conn = pymysql.connect(host='192.168.131.13', port=3306, user='root', password='zxsoft0#', db='sdn',
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    # 通过cursor创建游标
    cursor = conn.cursor()
    # 执行数据查询(查询当天的用户)
    sql = 'select username, userIDNumber, userNumber, iccid, insertDate' \
          ' from vpn_user u ' \
          ' right join vpn_card c on u.realNumber = c.realNumber' \
          ' where date(c.insertDate) = curdate() %s' \
          ' order by c.insertDate desc'
    cursor.execute(sql % '')
    # sql = 'select username, userIDNumber, userNumber, iccid, insertDate' \
    #       ' from vpn_user u ' \
    #       ' right join vpn_card c on u.realNumber = c.realNumber' \
    #       ' where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(insertDate)' \
    #       ' order by c.insertDate desc'
    # cursor.execute(sql)
    # 查询数据库数据
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    if result.__len__() == 0:
        return result
    return result


# update the users' info who be inserted at today
def update_user_info(users):
    global user_data_count

    if users is None:
        user_data_count = {}

    new_user_data_count = {}
    for user in users:
        user_id_number = user['userIDNumber']
        if user_data_count.keys().__contains__(user_id_number):
            new_user_data_count[user_id_number] = user_data_count[user_id_number]
        else:
            new_user_data_count[user_id_number] = (0, user)
    user_data_count = new_user_data_count


# fetch the user who has minimum count
def fetch_min_user_info():
    maxsize = sys.maxsize
    min_user = None
    for k in user_data_count.keys():
        count, user = user_data_count[k]
        if count < maxsize:
            maxsize, min_user = count, user
    return min_user


# increase user's count after assign a data
def increase(user_id_number):
    global user_data_count
    count, user = user_data_count[user_id_number]
    user_data_count[user_id_number] = count + 1, user


# index data
def index(data_list):
    actions = []
    i = 1
    for data in data_list:
        sql_data = fetch_min_user_info()
        if sql_data is None:
            raise Exception('there is no user.')
        increase(sql_data['userIDNumber'])
        src_ip = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(
            random.randint(0, 255)) + '.' + str(random.randint(0, 255))
        des_ip = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(
            random.randint(0, 255)) + '.' + str(random.randint(0, 255))
        src_port = str(random.randint(1000, 9999))
        des_port = str(random.randint(1000, 9999))

        c_time = '';
        try:
            c_time = datetime.datetime.strptime(str(data['timestamp']), '%Y-%m-%dT%H:%M:%S.%fZ');
        except Exception:
            c_time = datetime.datetime.strptime(str(data['timestamp']), '%Y-%m-%dT%H:%M:%SZ');
        p_time = c_time.strftime('%Y-%m-%d %H:%M:%S')

        title = ''
        try:
            title = data['title']
        except Exception:
            pass
        content = ''
        try:
            content = data['content']
        except Exception:
            pass
        url = ''
        try:
            url = data['url']
        except Exception:
            pass
        domain_name = ''
        try:
            domain_name = data['domainname']
        except Exception:
            pass

        action = {
            "_index": "tekuan",
            "_type": "record",
            "_id": data['id'],
            "_source": {
                'url': url,
                'title': title,
                'domain_name': domain_name,
                'size': content.__len__(),
                'content': content,
                'timestamp': p_time,

                'username': sql_data['username'],
                'identity_id': sql_data['userIDNumber'],
                'phone_num': sql_data['userNumber'],
                'ICCID': sql_data['iccid'],

                'src_ip': src_ip,
                'des_ip': des_ip,
                'src_port': src_port,
                'des_port': des_port,
                'header': 'HTTP/1.1',
                'protocol_type': random_protocol_by_weight(),
                'flow_type': flow_list[random.randint(0, flow_list.__len__() - 1)],
                'resource_type': random_resource_by_weight()
            }
        }
        i += 1
        actions.append(action)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    es = Elasticsearch(hosts=['192.168.131.12', '192.168.131.13', '192.168.131.15', '192.168.131.16'])
    helpers.bulk(es, actions)
    print('%s: insert into es data %d' % (now, i))


def request_data():
    data = []
    try:
        # time_from = '2018-05-15T00:00:00Z'
        # time_to = '2018-05-16T00:00:00Z'
        today = datetime.datetime.today()
        time_from = today.strftime('%Y-%m-%dT00:00:00Z')
        time_to = '*'
        url = 'http://192.168.32.11:8983/solr/sentiment/select?q=*:*&fq=country_code:0&fq=timestamp:[%s TO %s]' \
              '&rows=2000&wt=json' % (time_from, time_to)
        r = requests.get(url, verify=False)
        r = r.json()['response']['docs']
        r = json.dumps(r, ensure_ascii=False)
        data = json.loads(r)
    except Exception:
        pass
    return data


def fun_timer():
    # update_user_info(get_user_info())
    # index(request_data())

    update_user_info(get_user_info())
    try:
        index(request_data())
    except Exception:
        pass

    global timer
    timer = threading.Timer(600, fun_timer)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(0, fun_timer)
    timer.start()

# update_user_info(get_user_info())
# index(request_data_self())
