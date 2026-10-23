"""Bounded keyset pagination; cursors grant no access and are always re-authorised."""
import base64
import json
import re

def page_limit(value,default=24,maximum=100):
    if value is None:return default
    if type(value) is not int or not 1<=value<=maximum:raise ValueError('Page size must be between 1 and '+str(maximum))
    return value

def encode_cursor(scope,key):
    return base64.urlsafe_b64encode(json.dumps([scope,key],separators=(',',':')).encode()).decode().rstrip('=')

def decode_cursor(value,scope):
    if value is None:return None
    try:
        if not isinstance(value,str) or not 1<=len(value)<=400 or not re.fullmatch('[A-Za-z0-9_-]+',value):raise ValueError()
        data=json.loads(base64.urlsafe_b64decode(value+'='*(-len(value)%4)))
        if not isinstance(data,list) or len(data)!=2 or data[0]!=scope:raise ValueError()
        key=data[1]
        if not isinstance(key,list) or len(key)!=2 or type(key[0]) is not int or key[0]<0 or not isinstance(key[1],str) or not re.fullmatch('[a-f0-9]{32}',key[1]):raise ValueError()
        return key
    except (ValueError,TypeError,UnicodeError):raise ValueError('Invalid page cursor') from None
