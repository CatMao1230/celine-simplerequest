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
