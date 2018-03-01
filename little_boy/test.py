#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from gridfs import GridFS
import bson.binary
from util.logger import get_console_logger
from little_boy.client import BaseClient
from pymongo import MongoClient


def enum(**enums):
    return type('Enum', (), enums)

Urls = enum(
    excel_parse='file/parser'
)


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


class DataParserException(Exception):
    def __init__(self, msg, status=1):
        self.msg = msg
        self.status = status

    def __str__(self):
        return self.msg


class DataParser(BaseClient):
    """
    DataParser交互模块
    """

    CONF_SECTION = "data_parser"
    KEY_NAME = "url"

    def __init__(self):
        BaseClient.__init__(self, 'http://localhost:8080')

        self.dp_file_db_name = "excel_file"
        self.dp_file_mongo_url = "mongodb://127.0.0.1:27017"

    def _request(self, short_uri, payload):

        res = self._do_request(short_uri, payload)

        try:
            result = res.json()
        except Exception, e:
            get_console_logger().error(
                'data-parse response error, request: %s, param: %s, %s, %s',
                short_uri, payload, e.message, res.text
            )

            raise e

        if result['status'] != '0' or result['errstr']:
            get_console_logger().error(
                'data-parse response error, request: %s, param: %s, result: %s',
                short_uri, payload, result
            )
            print result
            print result.get('errstr', 'no_errstr')
            raise DataParserException(result.get('errstr', 'no_errstr'))

        return result['result']

    def mongo_file_preview(self, excel_id, file_type, row_offsets, sheet_names, excel_upload_config={}):
        payload = dict(
            excel_id=excel_id,
            file_type=file_type,
            mongo_urls="mongodb://127.0.0.1:27017",
            file_db_name=self.dp_file_db_name,
            file_mongo_url=self.dp_file_mongo_url,
            row_offsets=','.join(map(str, row_offsets)),
            sheet_names=",".join(sheet_names),
            excel_upload_config=json.dumps(excel_upload_config),
            is_preview=True
        )
        return self._request(Urls.excel_parse, payload)

    def mongo_file_parser(self, excel_id, file_type, dp_data_db_name, row_offsets, sheet_names, excel_upload_config={}):
        payload = dict(
            excel_id=excel_id,
            file_type=file_type,
            mongo_urls="mongodb://127.0.0.1:27017",
            file_db_name=self.dp_file_db_name,
            file_mongo_url="mongodb://127.0.0.1:27017",
            data_db_name=dp_data_db_name,
            row_offsets=','.join(map(str, row_offsets)),
            sheet_names=','.join(sheet_names),
            excel_upload_config=json.dumps(excel_upload_config),
            is_preview=False
        )
        return self._request(Urls.excel_parse, payload)


def put_file(file_path, excel_id):
    db = MongoClient('mongodb://127.0.0.1:27017')['excel_file']
    with open(file_path, 'r') as f:
        file_data = f.read()
        fs = GridFS(db)
        fs.put(bson.binary.Binary(file_data), filename=excel_id)


if __name__ == '__main__':
    data_parser = DataParser()
    excel_id = 'ex_6c5bb25518e44a3ea838d27ec8f1df5c'
    file_path = '/Users/HaiZhi/kongchao/haizhi/python_work/kc_tests/little_boy/error_rename.xlsx'
    put_file(file_path, excel_id)

    config = dict()
    config['delimiter'] = ','
    config['udt'] = []
    preview_res = data_parser.mongo_file_preview(excel_id, '.XLSX', [], [], config)
    print json.dumps(preview_res, indent=2)
