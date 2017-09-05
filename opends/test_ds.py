#!/usr/bin/python
# -*- coding: utf8 -*-

import unittest
from opends import OpenDS

ds_name = "test_opends_ds"


class TestTable(unittest.TestCase):
    def setUp(self):
        sdk = OpenDS()
        self.ds_id = self.ds_name_exists(ds_name)
        if self.ds_id:
            sdk.ds_delete(self.ds_id)
        self.ds_id = sdk.ds_create(ds_name)["ds_id"]



    def ds_name_exists(self, ds_name):
        sdk = OpenDS()
        ds_list = sdk.ds_list()["data_source"]
        for ds in ds_list:
            if ds_name == ds["name"]:
                return ds["ds_id"]
        return None

    # @unittest.skip("showing method skipping")
    def test_delete(self):
        sdk = OpenDS()
        sdk.ds_delete(self.ds_id)

    def test_status(self):
        sdk = OpenDS()
        sdk.ds_status(self.ds_id, OpenDS.DS_STATUS_ERROR, "test")

    def test_create_tb(self):
        sdk = OpenDS()
        sdk.tb_create()

if __name__ == '__main__':
    unittest.main()
