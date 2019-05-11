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

if __name__ == '__main__':
    unittest.main()