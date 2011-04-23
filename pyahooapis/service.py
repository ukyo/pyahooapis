#coding: utf-8

import re
import urllib
import urllib2
from xml.dom import minidom

import utils

json = utils.import_json()


newline_sub = re.compile('\n').sub
property_match = re.compile('[a-zA-Z].*').match

class Service(object):
    
    def __init__(self, appid, url):
        self.appid = appid
        self.url = url

    def get_text(self, node, tagName):
        try:
            return node.getElementsByTagName(tagName)[0].firstChild.nodeValue
        except:
            return None
    
    def _response(self, params):
        return urllib2.urlopen(self.url, data='appid=%s&%s' % (self.appid, urllib.urlencode(params))).read()
        
    def _setParam(self, params, param, name, split):
        if param is not None:
            params[name] = split.join(map(str, param))
    
    def get_dom(self, params):
        return minidom.parseString(self._remove_newline(self._response(params)))
        
    def _remove_newline(self, xml):
        return newline_sub('', xml)
    
    def _binary2list(self, binary, dct):
        return [dct[key] for key in iter(dct) if binary & key]
    
    def binary2param(self, split, binary, dct):
        return split.join(map(str, self._binary2list(binary, dct)))
        
    def py2json(self, obj):
        def _py2json(_obj):
            if isinstance(_obj, list):
                return [_py2json(_o) for _o in _obj]
            elif isinstance(_obj, BaseObject):
                propertys = (p for p in dir(_obj) if property_match(p))
                return dict((p, _py2json(getattr(_obj, p))) for p in propertys)
            else:
                return _obj
        return json.dumps(_py2json(obj), indent=False)
                
class BaseObject(object):
    pass

