#!/usr/bin/python
# -*- coding: utf8 -*-

import unittest
from opends import OpenDS

ds_name = "test_opends_ds"
tb_name = "test_opends_tb"

schema = [
        {
            "remark": "",
            "name": "id",
            "type": "number",
            "title": "ident"
        },
        {
            "remark": "",
            "name": "name",
            "type": "string"
        },
        {
            "remark": "",
            "name": "height",
            "type": "number"
        },
        {
            "remark": "",
            "name": "join_time",
            "type": "date"
        },
        {
            "remark": "",
            "name": "mark",
            "type": "string",
            "title": "words"
        }
    ]


class TestTb(unittest.TestCase):
    def setUp(self):
        sdk = OpenDS()
        self.ds_id = self.ds_name_exists(ds_name)
        if self.ds_id:
            sdk.ds_delete(self.ds_id)
        self.ds_id = sdk.ds_create(ds_name)["ds_id"]

        # init table

        self.tb_id = self.tb_name_exists()
        if self.tb_id:
            sdk.tb_delete(self.tb_id)
        self.tb_id = sdk.tb_create(self.ds_id, tb_name, schema, [])

    def tb_name_exists(self):
        sdk = OpenDS()
        tb_list = sdk.tb_list(self.ds_id)
        for table in tb_list:
            if table["name"] == tb_name:
                return table["tb_id"]
        return None

    def ds_name_exists(self, ds_name):
        sdk = OpenDS()
        ds_list = sdk.ds_list()["data_source"]
        for ds in ds_list:
            if ds_name == ds["name"]:
                return ds["ds_id"]
        return None

    def test_hehe(self):
        # folder_3802d78711587de8621076fa94f29c79
        pass


if __name__ == '__main__':
    unittest.main()
