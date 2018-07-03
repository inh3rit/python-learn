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
protocol_list = ['HTTP', 'HTTPS', 'FTP', 'SMTP', 'POP3', 'P2P']
# 流量类型
flow_list = ['上行', '下行']
# 资源类型
resource_list = ['HTML', 'CSS', '图片', '语音', '视频', 'FLASH']

es = Elasticsearch(['192.168.131.13', '192.168.131.12', '192.168.131.15', '192.168.131.16'])

user_data_count = {}


def get_user_info():
    # 连接MySQL数据库
    connection = pymysql.connect(host='192.168.131.13', port=3306, user='root', password='zxsoft0#', db='sdn',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    # 通过cursor创建游标
    cursor = connection.cursor()
    # 执行数据查询
    sql = 'select username, userIDNumber, userNumber, iccid, insertDate' \
          ' from vpn_user u ' \
          ' right join vpn_card c on u.realNumber = c.realNumber' \
          ' where date(c.insertDate) = curdate() %s' \
          ' order by c.insertDate desc'
    cursor.execute(sql % '')
    # 查询数据库数据
    result = cursor.fetchall()

    if result.__len__() == 0:
        cursor.execute(sql % '-1')
        result = cursor.fetchall()
    connection.close()
    return result


# update all user info for today's data
def update_user_info(users):
    global user_data_count

    new_user_data_count = {}
    for user in users:
        user_id_number = user['userIDNumber']
        if (user_data_count.keys().__contains__(user_id_number)):
            new_user_data_count[user_id_number] = user_data_count[user_id_number]
        else:
            new_user_data_count[user_id_number] = (0, user)
    user_data_count = new_user_data_count


# fetch the user who has minimum count
def fetch_min_user_info():
    min = sys.maxsize
    min_user = None
    for k in user_data_count.keys():
        count, user = user_data_count[k]
        if count < min:
            min, min_user = count, user
    return min_user


# increase user's count after assign a data
def increase(user_id_number):
    global user_data_count
    count, user = user_data_count[user_id_number]
    user_data_count[user_id_number] = count + 1, user


# index data
def index(list):
    if list.__len__() == 0:
        return
    actions = []
    i = 1
    for data in list:
        sql_data = fetch_min_user_info()
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
            "_id": i,
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
                'protocol_type': protocol_list[random.randint(0, protocol_list.__len__() - 1)],
                'flow_type': flow_list[random.randint(0, flow_list.__len__() - 1)],
                'resource_type': resource_list[random.randint(0, resource_list.__len__() - 1)]
            }
        }
        i += 1
        actions.append(action)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('%s: insert into es data %d' % (now, i))
    helpers.bulk(es, actions)


def request_data():
    data = []
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.get("http://36.7.150.150:7900/latest1hour", headers=headers)
        s = r.content.decode('utf8')
        data = json.loads(s)
    except Exception:
        pass
    return data


def fun_timer():
    update_user_info(get_user_info())
    index(request_data())

    global timer
    timer = threading.Timer(600, fun_timer)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(0, fun_timer)
    timer.start()

# fun_timer()
request_data()
