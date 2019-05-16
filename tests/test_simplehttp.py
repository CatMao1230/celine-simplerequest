# -*- coding: UTF-8 -*-
import unittest
import sys
import simplehttp

class GetJsonTest(unittest.TestCase):
    def test_url(self):
        r = simplehttp.get_json('https://httpbin.org/get')
        self.assertEqual(r['args'], {})

    def test_url_with_params(self):
        r = simplehttp.get_json('https://httpbin.org/get?debug=true')
        self.assertEqual(r['args'], {'debug': 'true'})

    def test_url_with_other_params(self):
        params = {'name': 'Celine'}
        r = simplehttp.get_json('https://httpbin.org/get?debug=true', params=params)
        self.assertEqual(r['args'], {'debug': 'true', 'name': 'Celine'})

    def test_url_with_params_in_chinese(self):
        params = {'name': u'常見問題 Q&A'}
        r = simplehttp.get_json('https://httpbin.org/get', params=params)
        self.assertEqual(r['args'], params)

class PostJsonTest(unittest.TestCase):
    def test_url_with_params(self):
        params = {'debug': 'true'}
        r = simplehttp.post_json('https://httpbin.org/post', params=params)
        self.assertEqual(r['args'], params)

    def test_url_with_params_and_data(self):
        params = {'debug': 'true'}
        data = {'isbn': '9789863479116', 'name': 'Celine'}
        r = simplehttp.post_json('https://httpbin.org/post', params=params, data=data)
        self.assertEqual(r['args'], params)
        self.assertEqual(r['json'], data)

    def test_url_with_params_in_chinese(self):
        params = {'name': u'常見問題 Q&A'}
        r = simplehttp.get_json('https://httpbin.org/get', params=params)
        self.assertEqual(r['args'], params)

    def test_url_with_data_in_chinese(self):
        data = {'isbn': '9789863479116', 'title': u'流暢的 Python'}
        r = simplehttp.post_json('https://httpbin.org/post', data=data)
        self.assertEqual(r['json'], data)

class HttpErrorTest(unittest.TestCase):
    def test_http_error_400(self):
        try:
            simplehttp.get_json('https://httpbin.org/status/400')
        except Exception as err:
            self.assertEqual(type(err), simplehttp.HttpError)
            self.assertEqual(sys.exc_info()[1].status_code, 400)
        else:
            self.fail('HttpError not raised.')
