import re
import pandas as pd
import time

import requests


def is_reject(url):
    try:
        r = requests.get(url)
    except Exception as e:
        time.sleep(20)
        with open('notice.error.txt', 'a', encoding='utf-8') as f:
            f.write('{},{},{}\n'.format(code, title, date))
        return False
    text = r.text
    r1 = re.compile('(\d+)\s*票反对')
    r2 = re.compile('反对\s*(\d+)\s*票')
    r3 = re.compile('反对票\s*(\d+)\s*票')
    g1 = re.compile('(\d+)\s*票弃权')
    g2 = re.compile('弃权\s*(\d+)\s*票')
    g3 = re.compile('弃权票\s*(\d+)\s*票')
    for p in [r1, r2, r3, g1, g2, g3]:
        match = p.search(text)
        if not match:
            continue
        num = match.group(1)
        if int(num) > 0:
            return True
    return False


with open('notice.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 创造表dataframe df用以存储表项
df = pd.DataFrame(columns=['股票代码', '日期', '标题'])
for line in lines:
    line = line.strip('\n')
    notice = line.split('||')
    url = notice[2]
    date = notice[1].split('T')[0]
    title = notice[0]
    code = notice[2].split('/')[5]
    # print(url)
    if is_reject(url):
        print(code)
        df = df.append({'股票代码': code, '日期': date, '标题': title}, ignore_index=True)

df.to_csv('notice.reject.csv')
        # with open('notice.reject.txt', 'a') as f:
        #     f.write('{},{},{}\n'.format(code, title, date))
