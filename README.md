# [由淺入深 Python Packaging](https://hackmd.io/s/H1zCrzg3N)
## 簡介
透過創建一個新的 Python Package --- simplehttp 來學習 Python Package 的打包發布，詳細的建置步驟請看 [HackMD](https://hackmd.io/s/H1zCrzg3N#%E4%BB%A5-ltyournamegt-simplerequest-%E7%82%BA%E4%BE%8B%E5%AF%A6%E4%BD%9C)。
## 指令
### 打包上傳
1. 上傳前若還沒設置 [~/ .pypirc](https://docs.python.org/2/distutils/packageindex.html#the-pypirc-file) ，需先建置 [~/ .pypirc](https://docs.python.org/2/distutils/packageindex.html#the-pypirc-file) 用來設定登入資訊的設定檔。
   ```
   [distutils]
   index-servers =
     testpypi

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = <your username>
   password = <your password>
   ```

2. 打包成 `.whl` 與 `.tar.gz` 檔並上傳套件。
   ```cmd
   $ python setup.py sdist bdist_wheel --universal upload -r testpypi
   ```

### 測試
```cmd
$ python -m unittest discover
```