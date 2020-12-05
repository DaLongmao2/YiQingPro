import traceback
import parsel
import pymysql
import requests
import json
import time

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_{}'
news_url = 'https://channel.chinanews.com/cns/s/5013.shtml?pager=0&pagenum=30&_=1606445344877'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0",
    'Cookie': '__jsluid_s=394c5066fc716116f77de10dacfc6bed'
}


def get_conn():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='1122', port=3306, db='XinGuanTencent')
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

# 获取历史数据
def get_tencent_data_other():
    response = requests.get(url=url.format('other'), headers=headers)
    response_json = response.json()['data']
    # Json 转换为 Dict
    data_all = json.loads(response_json)
    history = {}
    # 全国历史信息
    for i in data_all['chinaDayList']:
        # 获取时间
        ds = '2020.{}'.format(i['date'])
        # 改数据格式
        tup = time.strptime(ds, "%Y.%m.%d")
        # 改数和数据库兼容的格式 存入数据库
        ds = time.strftime("%Y-%m-%d", tup)
        # 确诊人数
        confirm = i['confirm']
        # 疑似人数
        suspect = i['suspect']
        # 出院
        heal = i['heal']
        # 死亡
        dead = i['dead']
        # 汇总 以每天的时间作为 Key 信息作为 Value
        history[ds] = {'confirm': confirm, 'suspect': suspect, 'heal': heal, 'dead': dead}

    for i in data_all['chinaDayAddList']:
        ds = '2020.{}'.format(i['date'])
        # 改数据格式
        tup = time.strptime(ds, "%Y.%m.%d")
        # 改数和数据库兼容的格式 存入数据库
        ds = time.strftime("%Y-%m-%d", tup)
        # 确诊人数 新增
        confirm_add = i['confirm']
        # 疑似人数 新增
        suspect_add = i['suspect']
        # 出院 新增
        heal_add = i['heal']
        # 死亡 新增
        dead_add = i['dead']
        history[ds].update({'confirm_add': confirm_add, 'suspect_add': suspect_add, 'heal_add': heal_add, 'dead_add': dead_add})
    # for item in history.keys():
    #     print(item)
    #     print(history[item])
    return history


# 获取详细数据
def get_tencent_data_h5():
    response = requests.get(url=url.format('h5'), headers=headers)
    response_json = response.json()['data']
    # Json 转换为 Dict
    data_all = json.loads(response_json)
    # 当日数据 详细数据
    details = []
    # 更新时间
    update_time = data_all['lastUpdateTime']
    # 在国家中获取 中国
    data_country = data_all['areaTree']
    # print(data_country)
    for pro_infos in data_country:
        # 获取省
        pro = pro_infos['children']
        for pro_name in pro:
            # 省名
            province = pro_name['name']
            for city_infos in pro_name['children']:
                # 城市名
                city = city_infos['name']
                confirm = city_infos['total']['confirm']
                suspect = city_infos['total']['suspect']
                heal = city_infos['total']['heal']
                dead = city_infos['total']['dead']
                details.append([update_time, province, city, confirm, suspect, heal, dead])
    return details

# 获取 新闻的 数据
# def get_tencent_data_news():
#     response = requests.get(url=news_url, headers=headers)
#     print(type(response.text))
#     print(response.text)

# 保存新闻数据
# def insert_news():
#     conn, cursor = get_conn()

def insert_history():
    conn, cursor = get_conn()
    try:
        dic = get_tencent_data_other()
        print(f"{time.asctime()}开始更新历史数据")
        sql = "insert into history values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                # 具体sql语句
                print(sql, [k, v.get('confirm'), v.get('confirm_add'), v.get('suspect'), v.get('suspect_add'),
                                     v.get('heal'), v.get('heal_add'), v.get('dead'), v.get('dead_add')])

                cursor.execute(sql, [k, v.get('confirm'), v.get('confirm_add'), v.get('suspect'), v.get('suspect_add'),
                                     v.get('heal'), v.get('heal_add'), v.get('dead'), v.get('dead_add')])
        conn.commit()
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)



def insert_details():
    conn, cursor = get_conn()
    try:
        li = get_tencent_data_h5()
        print(f"{time.asctime()}开始更新历史详细数据")
        sql = "insert into details values (null, %s, %s, %s, %s, %s, %s, %s)"
        # 查询数据库是否有该数据
        sql_query = "select %s=(select update_time from details order by id desc limit 1)"
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:
            for item in li:
                cursor.execute(sql, item)
                # 具体sql语句
                print(sql, item)
            conn.commit()
         # 更新最新数据完毕
        print(f"{time.asctime()}更新完成历史详细数据")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

if __name__ == '__main__':
    # insert_history()
    # insert_details()
    get_tencent_data_news()