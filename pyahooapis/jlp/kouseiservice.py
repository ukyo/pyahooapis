#coding: utf-8

from pyahooapis.service import Service, BaseObject

class KouseiService(Service):
    def __init__(self, appid):
        Service.__init__(self, appid, "http://jlp.yahooapis.jp/KouseiService/V1/kousei")
        
    def get_results(self,
                   sentence,
                   filter_group=(1,2,3),
                   no_filter=None,
                   json=False):
        
        params = {}
        
        params['sentence'] = sentence
        self._setParam(params, filter_group, 'filter_group', ',')
        self._setParam(params, no_filter, 'no_filter', ',')
        
        dom = self._getDOM(params)
        resultlist = [
                      Result(self._getText(r, 'StartPos'),
                             self._getText(r, 'Length'),
                             self._getText(r, 'Surface'),
                             self._getText(r, 'ShitekiWord'),
                             self._getText(r, 'ShitekiInfo'))
                      for r in dom.getElementsByTagName('Result')]
        
        return self.py2json(resultlist) if json else resultlist  
        
        
class Result(BaseObject):
    def __init__(self,
                 start_pos,
                 length,
                 surface,
                 shiteki_word,
                 shiteki_info):
        
        self.start_pos = int(start_pos)
        self.length = int(length)
        self.surface = surface
        self.shiteki_word = shiteki_word
        self.shiteki_info = shiteki_info
        
    def __str__(self):
        return self.surface.encode('utf8')
