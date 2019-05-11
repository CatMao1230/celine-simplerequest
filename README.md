# 由淺入深 Python Packaging

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
   ├── __init__.py # 此處需要 import mod
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
      $ python
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
1. 這裡要求套件只能使用 Python Standard Library，不能調用其他第三方套件。第一項要求的功能是：

   ```python
   $ python
   >>> import simplehttp
   >>> r = simplehttp.get_json('https://httpbin.org/get')
   >>> assert r['args'] == {}
   
   >>> params = {'name': 'Celine'}
   >>> r = simplehttp.get_json('https://httpbin.org/get?debug=true', params=params)
   >>> assert r['args'] == {'debug': 'true', 'name': 'Celine'}
   ```
2. 編輯 `__init__.py` ，上面 import 的部分，因為 urllib 在 python 2 和 3 之間的使用方法不同，所以需要分開 import 。
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