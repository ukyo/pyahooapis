#coding: utf-8

import re
import urllib
from xml.dom import minidom

import utils

json = utils.import_json()


newline_sub = re.compile('\n').sub
property_match = re.compile('[a-zA-Z].*').match

class Service(object):
    
    def __init__(self, appid, url):
        self.appid = appid
        self.url = url

    def _getText(self, node, tagName):
        try:
            return node.getElementsByTagName(tagName)[0].firstChild.nodeValue
        except:
            return None
    
    def _response(self, params):
        encParams = urllib.urlencode([(k, v) for k, v in params.iteritems()])
        f = urllib.urlopen(self.url + '?appid=' + self.appid + '&' + encParams)
        return f.read()
    
    def _setParam(self, params, param, name, split):
        if param is not None:
            params[name] = split.join(param)
    
    def _getDOM(self, params):
        return minidom.parseString(self._removeNewLine(self._response(params)))
        
    def _removeNewLine(self, xml):
        return newline_sub('', xml)
    
    def parseJSON(self, obj):
        def _parseJSON(_obj):
            if isinstance(_obj, list):
                return [_parseJSON(_o) for _o in _obj]
            elif isinstance(_obj, BaseObject):
                propertys = (p for p in dir(_obj) if property_match(p))
                return dict((p, _parseJSON(getattr(_obj, p))) for p in propertys)
            else:
                return _obj
        return json.dumps(_parseJSON(obj), indent=True)
                
class BaseObject(object):
    pass

