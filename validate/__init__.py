#!/usr/bin/env python
# -*- coding: utf-8 -*-
import StringIO
import gzip
import json
import os
import sys
import urllib
import requests

headers = {
    # 'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'Content-Encoding': 'gzip',
    'User-Agent': 'tongbubao-offline',
}
# headers = {
#     'Content-type': 'application/html;charset=UTF-8',
#     # 'Content-Encoding': 'gzip',
#     'User-Agent': 'tongbubao-offline',
# }
opends_api_url_prefix = os.environ.get("TBB_URL") or 'http://dev01.haizhi.com:65442/api'

payload = {
    'access_token': u'ae7509d4ac6be649126abb0bd64fb7a5',
    'tb_id': u'tb_3ad57f024d4442239c15f1a33bd0a060',
    'excel_id': u'ex_cb375c9dffa942f28ae8ffb286dddcd0 ',
    'map_id': u'map_5244640041a94f6b82a87236663e8db8',
    'rebuild_now': 0,
    'sheet_name': u'Sheet1'
}

params = {
    'access_token': u'ae7509d4ac6be649126abb0bd64fb7a5',
    'tb_id': u'tb_3ad57f024d4442239c15f1a33bd0a060',
    'excel_id': u'ex_\ncb375c9dffa942f28ae8ffb286dddcd0 ',
    'map_id': u'map_5244640041a94f6b82a87236663e8db8',
    'rebuild_now': '0',
    'sheet_name': u'Sheet1'
}

payload_str = json.dumps(payload)
# gzip
s = StringIO.StringIO()
g = gzip.GzipFile(fileobj=s, mode='w')
g.write(payload_str)
g.close()

# suffix = "/excel/replaceone"
suffix = "/excel/upload"
url = opends_api_url_prefix + suffix
# res = requests.post(url, headers=headers, data=payload)
file_path = u'中文.csv'
# file_path = u'english.csv'
print type(file_path), type(file_path.decode("utf-8"))
print urllib.quote_plus(file_path.encode("utf-8"))
res = requests.post(url, headers=headers, params=payload,
                    files={'file': (file_path.encode("utf-8"), open(file_path, 'rb'),)})
# res = requests.post(url, headers=headers, data=payload)
if res.status_code != 200:
    raise Exception("http error" + str(res.status_code))
result = json.loads(res.text)
print json.dumps(result, indent=2)
