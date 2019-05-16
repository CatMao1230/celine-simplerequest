import sys
import json
try:
    import urllib.parse as urllib
except ImportError:
    import urllib as urllib
try:
    import urllib.request as urlrequest
except ImportError:
    import urllib2 as urlrequest

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
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return 'HTTP Status Code: %s' % self.status_code

def get_json(url, **args):
    '''
    To get url's response by GET method.

    Args:
        url (string): The target url.
        **args:
            params (dict): The parameters of GET method.

    Returns:
        info (dict): Convert url's response to dict.

    Raises:
        HttpError: Can't open url.
    '''
    if args.setdefault('params', {}):
        args['params'] = {k: v.encode('utf-8') for k, v in args['params'].items()}
        url += '&' if '?' in url else '?'
        url += urllib.urlencode(args['params'])
    req = urlrequest.Request(url)
    try:
        res = urlrequest.urlopen(req)
        info = json.loads(res.read())
    except urlrequest.HTTPError as err:
        reraise(HttpError, HttpError(err.code), sys.exc_info()[2])
    return info

def post_json(url, **args):
    '''
    To get url's response by POST method.

    Args:
        url (string): The target url.
        **args:
            params (dict): The parameters of POST method.
            data (dict): The data of POST method.

    Returns:
        info (dict): Convert url's response to dict.

    Raises:
        HttpError: Can't open url.
    '''
    if args.setdefault('params', {}):
        args['params'] = {k: v.encode('utf-8') for k, v in args['params'].items()}
        url += '&' if '?' in url else '?'
        url += urllib.urlencode(args['params'])

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(args.setdefault('data', {})).encode('utf-8')
    req = urlrequest.Request(url=url, data=data, headers=headers)
    try:
        res = urlrequest.urlopen(req)
        info = json.loads(res.read())
    except urlrequest.HTTPError as err:
        reraise(HttpError, HttpError(err.code), sys.exc_info()[2])
    return info
