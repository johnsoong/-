
import json
import datetime
import time
import sys
import re

import requests


def get_notice_list(date_time='2015-01-01', page_size=50, page_index=1):
    results = []

    payload = {
        'time': date_time,
        'PageSize': page_size,
        'PageIndex': page_index,
        'rt': '50821627',
        'SecNodeType': 0,
        'jsObj': 'jqNVhyQg',
        'CodeType': 1,
        'FirstNodeType': 0,
        'StockCode': ''
    }
    for i in range(20):
        try:
            r = requests.get('http://data.eastmoney.com/notices/getdata.ashx', params=payload)
            break
        except Exception as e:
            time.sleep(20)
            continue

    try:
        js = r.text
        data = js[js.index('{'):(len(js) - 1)]
        data_dict = json.loads(data)
        if not data_dict['data']:
            return results
        results.extend(data_dict['data'])
    #   若出错，则是网站并发存在问题，等10s继续访问
    except Exception as e:
        time.sleep(10)
        return get_notice_list(date_time, page_size, page_index)
    return results


def get_notices(date_time='2015-01-01'):
    notices = []
    index = 0
    while True:
        index = index + 1
        print('Get {}: page index {}'.format(date_time, index))
        with open('notice.log', 'a') as log:
            log.write('Get {}: page index {}\n'.format(date_time, index))
        notice_list = get_notice_list(date_time=date_time, page_index=index)
        if len(notice_list) == 0:
            break

        r1 = re.compile('董事会')
        r2 = re.compile('会议决议')

        for notice in notice_list:
            # 查询公告类型是否为‘董事会决议公告’
            # if notice['ANN_RELCOLUMNS'][0]['COLUMNNAME'] == '董事会决议公告':
            #     notices.append(dict(title=notice['NOTICETITLE'], url=notice['Url'], date=notice['NOTICEDATE']))
            # 确认标题字段是否包含'董事会'与'决议公告'
            if (r1.search(notice['NOTICETITLE']) is not None) and (r2.search(notice['NOTICETITLE']) is not None):
                notices.append(dict(title=notice['NOTICETITLE'], url=notice['Url'], date=notice['NOTICEDATE']))

    return notices


def get_data_times(end_tag='2015-12-31'):
    end = datetime.datetime.strptime(end_tag, '%Y-%m-%d')
    start = datetime.datetime.strptime('2015-12-31', '%Y-%m-%d')
    delta = datetime.timedelta(days=1)
    tags = [end_tag]
    while True:
        end = end - delta
        if end < start:
            break
        tags.append(end.strftime('%Y-%m-%d'))

    return tags

# 返回的days存储所有2005-1-1到end tag这一字符串下所有的日期
days = get_data_times(end_tag='2016-12-31')

#
for day in days:
    # 针对每一个日期，返回该日期下所找到的条目及其属性
    notices = get_notices(day)
    for notice in notices:
        # print(notice)
        with open('notice.txt', 'a', encoding='utf-8') as f:
            f.write('{}||{}||{}\n'.format(notice['title'], notice['date'], notice['url']))
            print(notice['url'])
0
