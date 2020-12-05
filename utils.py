#!/usr/bin/env python
# encoding: utf-8
import random
import time
import pymysql


def get_conn():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='1122', port=3306, db='XinGuanTencent')
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    return res


def get_time():
    # 获取当前的系统时间戳
    dt = time.strftime('%Y-%m-%d %X')
    return dt


# 获取center1
def get_center1():
    # 查询详情
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal), " \
          "sum(dead) from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1)"
    res = query(sql)
    print(res)
    # ((Decimal('92578'), 1, Decimal('87281'), Decimal('4749')),)
    #
    return res[0]


def get_center2():
    sql = 'select province, sum(confirm) from details where update_time=(select  update_time from details order by update_time desc limit 1) group by province'
    res = query(sql)
    print(res)
    return res


def get_left1():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


def get_left2():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res


def get_right1():
    """
    :return:  返回非湖北地区城市确诊人数前5名
    """
    sql = 'SELECT city,confirm FROM ' \
          '(select city,confirm from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'ORDER BY confirm DESC LIMIT 5'
    res = query(sql)
    return res

def get_right2():
    num = random.randint(1, 20)
    res = (((f'比如种族歧视问题。当前美国疫情仍在蔓延，社交媒体上针对亚裔的情绪宣泄依然不时可见，亚裔依然遭受着或者赤裸裸或者隐性的偏见与歧视的困扰{num}',), (f'病毒基因测序提示满洲里市新冠肺炎疫情由境外输入引起满洲里的2个新冠病毒病例是由境外输入引起。下一步，内蒙古将对本起疫情进行溯源，对其他确诊病例也要进行基因测序和比对{num}',), (f'吴尊友：喀什疫情源头是境外集装箱 无症状感染者成导火索{num}',), (f'记者从内蒙古自治区满洲里市新冠肺炎疫情防控工作指挥部获悉，该市将开启第二轮全员核酸检测工作{num}',)))
    return res

if __name__ == '__main__':
    get_center2()
