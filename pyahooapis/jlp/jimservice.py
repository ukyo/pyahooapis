#coding: utf-8
from pyahooapis.service import Service, BaseObject

FORMAT_ROMAN = 'roman'

MODE_NORMAL = 'normal'
MODE_ROMAN = 'roman'
MODE_PREDICTIVE = 'predictive'

RESPONSE_KATAKANA = 1
RESPONSE_HIRAGANA = 2
RESPONSE_ALPHANUMERIC = 4
RESPONSE_HALF_KATAKANA = 8
RESPONSE_HALF_ALPHANUMERIC = 16

RESPONSES = {
    RESPONSE_KATAKANA : 'katakana',
    RESPONSE_HIRAGANA : 'hiragana',
    RESPONSE_ALPHANUMERIC : 'alphanumeric',
    RESPONSE_HALF_KATAKANA : 'half_katakana',
    RESPONSE_HALF_ALPHANUMERIC : 'half_alphanumeric',
    }

DICTIONARY_DEFAULT = 1
DICTIONARY_NAME = 2
DICTIONARY_PLACE = 4
DICTIONARY_ZIP = 8
DICTIONARY_SYMBOL = 16

DICTIONARIES = {
    DICTIONARY_DEFAULT : 'default',
    DICTIONARY_NAME : 'name',
    DICTIONARY_PLACE : 'place',
    DICTIONARY_ZIP : 'zip',
    DICTIONARY_SYMBOL : 'symbol',
    }

class JIMService(Service):
    
    def __init__(self, appid):
        Service.__init__(self, appid, 'http://jlp.yahooapis.jp/JIMService/V1/conversion')
    
    def get_segments(self,
                       sentence,
                       format=None,
                       mode=None,
                       response=None,
                       dictionary=None,
                       results=999,
                       json=False):
        
        params = {}
        params['sentence'] = sentence
        if format is not None:
            params['format'] = format
        if mode is not None:
            params['mode'] = mode
        if response is not None:
            params['response'] = self._binary2param(',', response, RESPONSES)
        if dictionary is not None:
            params['dictionary'] = self._binary2param(',', dictionary, DICTIONARIES)
        if results is not None:
            params['results'] = str(results)
        
        dom = self._get_dom(params)
        
        segmentlist = [
                       Segment(self._get_text(s, 'SegmentText'),
                               self._get_text(s, 'Alphanumeric'),
                               self._get_text(s, 'HalfAlphanumeric'),
                               self._get_text(s, 'Katakana'),
                               self._get_text(s, 'HalfKatakana'),
                               self._get_text(s, 'Hiragana'),
                               [c.firstChild.nodeValue for c in s.getElementsByTagName('Candidate')])
                       for s in dom.getElementsByTagName('Segment')]
        
        return self.py2json(segmentlist) if json else segmentlist


class Segment(BaseObject):
    def __init__(self,
                 segment_text,
                 alphanumeric=None,
                 half_alphanumeric=None,
                 katakana=None,
                 half_katakana=None,
                 hiragana=None,
                 candidate_list=[]):
        
        self.segment_text = segment_text
        self.alphanumeric = alphanumeric
        self.half_alphanumeric = half_alphanumeric
        self.katakana = katakana
        self.half_katakana = half_katakana
        self.hiragana = hiragana
        self.candidate_list = candidate_list
    
    def __str__(self):
        return self.segment_text.encode('utf8')


