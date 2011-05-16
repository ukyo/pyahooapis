#coding: utf-8

from pyahooapis.service import Service, BaseObject

FILTER_GROUP_MISS = 1
FILTER_GROUP_SIMPLIFY = 2
FILTER_GROUP_TO_BETTER = 4

FILTER_GROUPS = {
    FILTER_GROUP_MISS : 1,
    FILTER_GROUP_SIMPLIFY : 2,
    FILTER_GROUP_TO_BETTER : 3,
    }

NO_FILTER_FALSE_CONVERSION = 1
NO_FILTER_MISUSE = 2
NO_FILTER_USE_ATTENTION = 4
NO_FILTER_UNPLEASANT = 8
NO_FILTER_DEPENDENCE = 16
NO_FILTER_FOREIGN_PLACE = 32
NO_FILTER_NAME = 64
NO_FILTER_NOT_RA = 128
NO_FILTER_KANJI_OUTSIDE_THE_TABLE = 256
NO_FILTER_PHRASEOLOGY = 512
NO_FILTER_PARAPHRASE = 1024
NO_FILTER_DOUBLE_NEGATION = 2048
NO_FILTER_NOT_PARTICLE = 4096
NO_FILTER_PLENASM = 8192
NO_FILTER_ABBREVIATION = 16384

NO_FILTERS = {
    NO_FILTER_FALSE_CONVERSION : 1,
    NO_FILTER_MISUSE : 2,
    NO_FILTER_USE_ATTENTION : 3,
    NO_FILTER_UNPLEASANT : 4,
    NO_FILTER_DEPENDENCE : 5,
    NO_FILTER_FOREIGN_PLACE : 6,
    NO_FILTER_NAME : 7,
    NO_FILTER_NOT_RA : 8,
    NO_FILTER_KANJI_OUTSIDE_THE_TABLE : 9,
    NO_FILTER_PHRASEOLOGY : 10,
    NO_FILTER_PARAPHRASE : 11,
    NO_FILTER_DOUBLE_NEGATION : 12,
    NO_FILTER_NOT_PARTICLE : 13,
    NO_FILTER_PLENASM : 14,
    NO_FILTER_ABBREVIATION : 15,
    }

class KouseiService(Service):
    url = "http://jlp.yahooapis.jp/KouseiService/V1/kousei"
        
    def get_results(self, sentence, filter_group=None, no_filter=None, json=False):
        params = {}
        
        params['sentence'] = sentence
        if filter_group is not None:
            params['filter_group'] = self._binary2param(',', filter_group, FILTER_GROUPS)
        if no_filter is not None:
            params['no_filter'] = self._binary2param(',', no_filter, NO_FILTERS)
        
        dom = self._get_dom(params)
        results = [
                      Result(self._get_text(r, 'StartPos'),
                             self._get_text(r, 'Length'),
                             self._get_text(r, 'Surface'),
                             self._get_text(r, 'ShitekiWord'),
                             self._get_text(r, 'ShitekiInfo'))
                      for r in dom.getElementsByTagName('Result')]
        
        return self.py2json(results) if json else results  
        
        
class Result(BaseObject):
    def __init__(self, start_pos, length, surface, shiteki_word, shiteki_info):
        
        self.start_pos = int(start_pos)
        self.length = int(length)
        self.surface = surface
        self.shiteki_word = shiteki_word
        self.shiteki_info = shiteki_info
        
    def __str__(self):
        return self.encode(self.surface)
