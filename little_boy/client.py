#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.logger import get_console_logger
import os
from urlparse import urlparse
from requests.sessions import Session
from requests.adapters import ReadTimeout
import time
from requests.exceptions import ConnectionError, HTTPError
from threading import local


class ConnectException(Exception):
    pass


class BaseException(Exception):

    def __init__(self, errstr, status=1, err_parameter={}, uri='', result=''):
        self.errstr = errstr
        self.status = status
        self.err_parameter = err_parameter
        self.uri = uri
        self.result = result

    def __str__(self):
        return '<%s: status %s, error %s, err_parameter %s, uri %s>' % (
            self.__class__.__name__, self.status, self.errstr, self.err_parameter, self.uri)


class BaseClient(object):

    _thread_vars = local()

    MODULE_NAME = ""

    PERFORMANCE = "performance"

    _global_sessions = {}

    @classmethod
    def set_trace_id(cls, trace_id):
        cls._thread_vars.trace_id = trace_id

    def __init__(self, url_prefix):
        self.url_prefix = url_prefix
        self.timeout = (60, 40*60)
        self.session_reuse = 1
        self.traceid_in_url = 0

    @classmethod
    def warn_out(cls, *args, **kwargs):
        get_console_logger().warning(*args, **kwargs)

    @classmethod
    def error_out(cls, *args, **kwargs):
        get_console_logger().error(*args, **kwargs)

    @classmethod
    def trace_out(cls, *args, **kwargs):
        get_console_logger().error(*args, **kwargs)

    def pre_params(self):
        return {}

    @classmethod
    def get_session(cls, url):

        """
        根据要访问的url找到合适的session，尽可能重用连接
        """

        urlkey = "://".join(urlparse(url)[0:2])

        if urlkey not in cls._global_sessions:
            cls._global_sessions[urlkey] = Session()

        return cls._global_sessions[urlkey]

    def _do_request(self, short_uri, payload, files=None):
        payload.update(self.pre_params())

        trace_id = getattr(self.__class__._thread_vars, "trace_id", "")

        # need put traceid in url
        if self.traceid_in_url:
            if len(short_uri.split('?')) == 1:
                short_uri += "?trace_id=%s" % trace_id
            else:
                short_uri += "&trace_id=%s" % trace_id
        # put traceid in body
        else:
            payload["trace_id"] = trace_id

        res = None
        url = os.path.join(self.url_prefix, short_uri)
        try:
            ts = time.time()

            if self.session_reuse:
                # 如果使用长连接，则复用session
                c_session = self.get_session(url)
            else:
                c_session = Session()

            params_dict = dict(data=payload, timeout=self.timeout)
            res = c_session.post(url, **params_dict)
            res.raise_for_status()
            tc = time.time() - ts

            self.trace_out("[%s] [%f] [%s]", url, tc, trace_id)

        except ConnectionError:
            # try_count += 1
            # time.sleep(1)
            self.warn_out("connect failed to %s [%s]", self.url_prefix, trace_id)
        except ReadTimeout:
            self.error_out("Timeout for url: %s [%s]", url, trace_id)
            raise
        except HTTPError:
            self.error_out("[%s] [%s] [%s] bad response[%s]", url, trace_id, res.status_code, res.text)
            if res.status_code == 504:
                raise

        if res is None:
            raise ConnectException("connect upstream error. all backend tried %s" % self.url_prefix)

        return res
