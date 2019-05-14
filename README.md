# [由淺入深 Python Packaging](https://hackmd.io/s/H1zCrzg3N)
## 簡介
透過創建一個新的 Python Package --- simplehttp 來學習 Python Package 的打包發布，詳細的建置步驟請看 [HackMD](https://hackmd.io/s/H1zCrzg3N#%E4%BB%A5-ltyournamegt-simplerequest-%E7%82%BA%E4%BE%8B%E5%AF%A6%E4%BD%9C)。
## 指令
### 打包上傳
1. 打包成 `.whl` 與 `.tar.gz` 檔至 `dist/`

   ```cmd
   $ python setup.py sdist bdist_wheel
   ```
2. 上傳前若還沒設置 [~/ .pypirc](https://docs.python.org/2/distutils/packageindex.html#the-pypirc-file) ，需先建置 [~/ .pypirc](https://docs.python.org/2/distutils/packageindex.html#the-pypirc-file) 用來設定登入資訊的設定檔。
   ```
   [distutils]
   index-servers =
     testpypi

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = <your username>
   password = <your password>
   ```
4. 將 `dist/` 下的打包檔上傳至 TestPyPI 。
   ```cmd
   $ python setup.py sdist upload -r testpypi
   ```
4. 可以合併成下面的指令，打包並上傳。
   ```cmd
   $ python setup.py sdist bdist_wheel upload -r testpypi
   ```

### 測試
```cmd
$ python -m unittest discover
```