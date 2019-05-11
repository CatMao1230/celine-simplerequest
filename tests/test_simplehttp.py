import unittest
import sys
sys.path.append('..')
import simplehttp

class GetJsonTest(unittest.TestCase):
    def test_url(self):
        r = simplehttp.get_json('https://httpbin.org/get')
        self.assertEqual(r['args'], {})

    def test_url_with_params(self):
        params = {'name': 'Celine'}
        r = simplehttp.get_json('https://httpbin.org/get?debug=true')
        assert r['args'] == {'debug': 'true'}

    def test_url_with_other_params(self):
        params = {'name': 'Celine'}
        r = simplehttp.get_json('https://httpbin.org/get?debug=true', params=params)
        assert r['args'] == {'debug': 'true', 'name': 'Celine'}

class PostJsonTest(unittest.TestCase):
    def test_url_with_params(self):
        params = {'debug': 'true'}
        r = simplehttp.post_json('https://httpbin.org/post', params=params)
        assert r['args'] == params
    def test_url_with_params_and_data(self):
        params = {'debug': 'true'}
        data = {'isbn': '9789863479116', 'name': 'Celine'}
        r = simplehttp.post_json('https://httpbin.org/post', params=params, data=data)
        assert r['args'] == params
        assert r['data'] == data

if __name__ == '__main__':
    unittest.main()