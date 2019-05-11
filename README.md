# [由淺入深 Python Packaging](https://hackmd.io/s/H1zCrzg3N)

## 建置步驟
1. 建立並啟動虛擬環境。

   ```cmd
   $ virtualenv venv
   $ source venv/bin/activate
   ```
2. 產生 [~/ .pypirc 檔](https://docs.python.org/2/distutils/packageindex.html#the-pypirc-file)，用來設定登入 testpypi 的設定檔，此處的帳號密碼填入申請好的 [TestPyPI](https://test.pypi.org/) 帳密。
   ```rc
   [distutils]
   index-servers =
       testpypi

    [testpypi]
    repository = https://test.pypi.org/legacy/
    username = <your username>
    password = <your password>
   ```
3. 建出以下檔案。
   ```
   <yourname>-simplerequest/
   ├── README.md
   ├── simplehttp/
   │   └── __init__.py
   └── setup.py
   ```
   `simplehttp/` 套件的部分說明，一個 python 檔案表是一個模組，而一個包含 `__init__` 的資料夾就可以視為一個套件，外部的使用者可以透過 `import simplehttp` 來使用，若 `simplehttp/` 下還有其他模組，如：
   ```
   simplehttp/
   ├── __init__.py
   └── mod.py
   ```
   則可以透過 `simplehttp.mod` 來呼叫。
4. 設定 `setup.py` 檔，更多的參數可以參考[官方文件](https://docs.python.org/2.7/distutils/setupscript.html#additional-meta-data)。
   ```python
   from setuptools import setup

   setup(
       name='<yourname>-simplerequest',
       version='1.0.0',
       author='<your name>',
       author_email='<your email>',
       description='A simple request.',
       url='<your github repo or other website>',
       packages=['simplehttp'],
       classifiers=[
           'Programming Language :: Python :: 2.7',
           'Programming Language :: Python :: 3'
      ],
   )
   ```
   特別說明 `packages` 的參數，表示要打包的套件有哪些，而 `classifiers` 內可以放入一些資訊，包括了支援的版本。
5. 此時已經可以將套件打包上傳至 TestPyPI ，要特別注意的是，一但上傳該套件，則此套件此版本不可再上傳，會出現命稱重複的錯誤，因次在每次上傳前，強烈建議先在本地安裝測試過再行上傳。
   ```error
   error: Upload failed (400): File already exists. See https://test.pypi.org/help/#file-name-reuse
   ```
   #### 本地測試
   1. 安裝 `setup.py` 。

      ```cmd
      $ python setup.py install
      ```
   2. 安裝成功後，測試套件是否可以運作。
      ```python
      >>> import simplehttp
      >>> ...
      ```

   #### 打包上傳
   1. 打包成 `.whl` 檔至 `dist/`
   
      ```cmd
      $ python setup.py sdist bdist_wheel
      ```
   2. 將 `dist/` 下的打包檔上傳至 TestPyPI 。
      ```cmd
      $ python setup.py sdist upload -r testpypi
      ```
   3. 可以合併成下面的指令，打包並上傳。
      ```cmd
      $ python setup.py sdist bdist_wheel upload -r testpypi
      ```
## 套件內容撰寫
### get_json()
1. 這裡要求套件只能使用 Python Standard Library，不能調用其他第三方套件。第一項要求的功能是：

   ```python
   >>> import simplehttp
   >>> r = simplehttp.get_json('https://httpbin.org/get')
   >>> assert r['args'] == {}
   
   >>> params = {'name': 'Celine'}
   >>> r = simplehttp.get_json('https://httpbin.org/get?debug=true', params=params)
   >>> assert r['args'] == {'debug': 'true', 'name': 'Celine'}
   ```
2. 編輯 `__init__.py` ，上面 import 的部分，因為 urllib 在 Python2 和 3 之間的使用方法不同，所以需要分開 import 。
   ```python
   #/usr/bin/env python
   # -*- coding: UTF-8 -*-
   import json
   try:
       import urllib.parse as urllib
   except ImportError:
       import urllib as urllib
   try:
       import urllib.request as urlrequest
   except ImportError:
       import urllib2 as urlrequest

   def get_json(url, **args):
       if args.setdefault('params', {}):
           url += '&' if '?' in url else '?'
           url += urllib.urlencode(args['params'])
       req = urlrequest.Request(url)
       res = urlrequest.urlopen(req)
       info = json.loads(res.read())
       return info
   ```
### Unittest
撰寫單元測試 unittest ，方便日後程式碼的維護開發。

1. 在專案資料夾下新增檔案。

   ```
   tests/
   ├── __init__.py # 此處需要 import simplehttp
   └── test_simplehttp.py
   ```
2. 編輯 `test_simplehttp.py` 。
   ```python
   import unittest
   import sys
   sys.path.append('..')
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

   if __name__ == '__main__':
       unittest.main()
   ```
3. 此時可以執行測試查看結果，自動找出某個資料夾底下所有的測試（預設會找 `test*.py` ）。
   ```cmd
   $ python -m unittest discover
   ```
   最後出現 OK 即為單元測試成功。
   
### post_json()
1. 第二項功能需求：
   ```python
   >>> params = {'debug': 'true'}
   >>> data = {'isbn': '9789863479116', 'name': 'Celine'}
   >>> r = simplehttp.post_json('https://httpbin.org/post', params=params, data=data)
   >>> assert r['args'] == params
   >>> assert r['json'] == data
   ```
3. 修改 `simplehttp/__init__.py` ，新增函式 post_json() 。

   ```python
   def post_json(url, **args):
       if args.setdefault('params', {}):
           url += '&' if '?' in url else '?'
           url += urllib.urlencode(args['params'])

       headers = {'Content-Type': 'application/json'}
       data = json.dumps(args.setdefault('data', {})).encode('utf-8')
       req = urlrequest.Request(url=url, data=data, headers=headers)
       res = urlrequest.urlopen(req)
       info = json.loads(res.read())
       return info
   ```
   其中 `encode('utf-8')` 可以參考[此文章](https://blog.csdn.net/IMW_MG/article/details/78555375)， Python3 中不能提交 str 類型，需為 type 類型。
3. 修改 `tests/test_simplehttp.py` ，新增單元測試。
   ```python
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
   ```

### 解決中文
1. 有另外一項需求是參數包含中文。

   ```python
   >>> params = {'name': u'常見問題 Q&A'}
   >>> r = simplehttp.get_json('https://httpbin.org/get', params=params)
   >>> assert r['args'] == params
   ```
2. 先新增這項 TestCase 至 `tests/test_simplehttp.py`。
   ```python
   #/usr/bin/env python
   # -*- coding: UTF-8 -*-
   ...
   class GetJsonTest(unittest.TestCase):
       ...
       def test_url_with_params_in_chinese(self):
           params = {'name': u'常見問題 Q&A'}
           r = simplehttp.get_json('https://httpbin.org/get', params=params)
           self.assertEqual(r['args'], params)
   ```
   此時執行 python2.7 會出現錯誤。
   ```error
   UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)
   ```
3. 修改 `simplehttp/__init__.py` ，get_json() 和 post_json() 都需修改，將 unicode 進行 utf-8 編碼。
   ```python
   if args.setdefault('params', {}):
        args['params'] = {k: v.encode('utf-8') for k, v in args['params'].items()}
        ...
   ```
4. 再新增一項 TestCase 至 `tests/test_simplehttp.py`。
   ```python
   class PostJsonTest(unittest.TestCase):
       ...
       def test_url_with_data_in_chinese(self):
            data = {'isbn': '9789863479116', 'title': u'流暢的 Python'}
            r = simplehttp.post_json('https://httpbin.org/post', data=data)
            self.assertEqual(r['json'], data)
   ```

### 自定義異常處理
1. 新的功能需要顯示出自定義的異常。
   
   ```python
   >>> simplehttp.get_json('https://httpbin.org/status/400')
   Traceback (most recent call last):
   ...
   simplehttp.HttpError: HTTP Status Code: 400
   
   >>> import sys
   >>> assert sys.last_value.status_code == 400
   ```
2. 可以先看這兩篇文章：[自訂例外](https://openhome.cc/Gossip/Python/UserDefinedException.html)、[例外兼容 Python2 與 Python3 的寫法](https://mozillazg.com/2016/08/python-the-right-way-to-catch-exception-then-reraise-another-exception.html#hidpython-2-python-3)。
3. 上面 `simplehttp.HttpError: HTTP Status Code: 400` 這段可以拆成三個部分：
   `[package name].[exception class]: [exception str]`。

4. 修改 `simplehttp/__init__.py` ，再 import 下方輸入程式碼，另外再新增一個 Class 繼承 Exception 。
   上半段的 if else 函式是[例外兼容 Python2 與 Python3 的寫法](https://mozillazg.com/2016/08/python-the-right-way-to-catch-exception-then-reraise-another-exception.html#hidpython-2-python-3)。
   ```python
   if sys.version_info[0] == 3:
       def reraise(tp, value, tb=None):
           if value.__traceback__ is not tb:
               raise value.with_traceback(tb)
           else:
               raise value
   else:
       exec('''def reraise(tp, value, tb=None):
           raise tp, value, tb
       ''')

   class HttpError(Exception):
       def __init__(self, code):
           self.code = code

       def __str__(self):
           return 'HTTP Status Code: %s' % self.code
   ```
5. 修改函式，發生錯誤時呼叫異常。
   ```python
   def get_json(url, **args):
       ...
       req = urlrequest.Request(url)
       try:
           res = urlrequest.urlopen(req)
           info = json.loads(res.read())
       except urlrequest.HTTPError as e:
           raise
       return info
   ```
6. 新增一項 TestCase 至 `tests/test_simplehttp.py`。
   ```python
   import sys
   ...
   class HttpErrorTest(unittest.TestCase):
       def http_error_400(self):
           simplehttp.get_json('https://httpbin.org/status/400')
           self.assertEqual(sys.last_value.status_code, 400)
   ```

## Travis CI
每次更新程式碼時，都要先本地測試，之後提交到 github ，然後再打包發佈到 PyPI ，過程相當繁瑣，而 github + travis-ci 可以解決這個問題，建構一個自動部署環境。

1. 先進入 [travis-ci](https://travis-ci.com/) 網站，可以直接以 Github 登入，並至 [travis-ci.com/profile](travis-ci.com/profile) 激活 repo 。
2. 在專案資料夾下，新增 `.travis.yml` 檔，參考 [Building a Python Project](https://docs.travis-ci.com/user/languages/python/) 與 [PyPI deployment](https://docs.travis-ci.com/user/deployment/pypi/)。

   ```
   language: python
   python:
   - '2.7'
   - '3.6'
   - '3.7'
   dist: xenial
   script: python -m unittest discover
   deploy:
     provider: pypi
     server: https://testpypi.python.org/pypi
     on:
       tags: true
     user: <your account>
   ```
   其中 `on:` 內的句子表示：在發佈新的版本才會打包發布。
3. 上方的 deploy 少了 password 的原因是：若直接將密碼打在檔案中十分危險，因此需要用 travis-encrypt 加密。
   ```cmd
   $ pip install travis-encrypt
   $ travis-encrypt --deploy gusibi python-weixin .travis.yml
   Password: 輸入密碼
   ```
   此時在看 `.travis.yml` ，會發現多出了加密的密碼。
4. 之後 push 到 github 時，都可以進入 Travis CI 網站查看建置狀況與結果。
