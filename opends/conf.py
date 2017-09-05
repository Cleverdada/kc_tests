#!/usr/bin/python
# -*- coding: utf8 -*-
Test = True

if Test:

    opends_api_url_prefix = 'http://dev01.haizhi.com:65442'
    # token = "ae7509d4ac6be649126abb0bd64fb7a5" # kongchao
    # domain = "haizhi"

    token = '925e4bb0a1b9b1b3e6045dda575de6ab'  # datatest
    domain = 'datatest'

else:
    opends_api_url_prefix = 'https://open.bdp.cn'
    token = "1aed84f0292c86010fc742fab90e7c43"
    domain = "haizhi"