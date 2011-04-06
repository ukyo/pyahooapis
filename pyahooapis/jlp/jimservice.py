from pyahooapis.service import Service, BaseObject


FORMAT_ROMAN = 'roman'


MODE_NORMAL = 'normal'
MODE_ROMAN = 'roman'
MODE_PREDICTIVE = 'predictive'


RESPONSE_KATAKANA = 'katakana'
RESPONSE_HIRAGANA = 'hiragana'
RESPONSE_ALPHANUMERIC = 'alphanumeric'
RESPONSE_HALF_KATAKANA = 'half_katakana'
RESPONSE_HALF_ALPHANUMERIC = 'half_alphanumeric'


DICTIONARY_DEFAULT = 'default'
DICTIONARY_NAME = 'name'
DICTIONARY_PLACE = 'place'
DICTIONARY_ZIP = 'zip'
DICTIONARY_SYMBOL = 'symbol'


class JIMService(Service):
    
    def __init__(self, appid):
        Service.__init__(self, appid, 'http://jlp.yahooapis.jp/JIMService/V1/conversion')
    
    def get_segments(self,
                       sentence,
                       format=None,
                       mode=MODE_NORMAL,
                       response=None,
                       dictionary=[DICTIONARY_DEFAULT],
                       results=999,
                       json=False):
        
        params = {}
        params['sentence'] = sentence
        self._setParam(params, format, 'format', '')
        params['mode'] = mode
        self._setParam(params, response, 'response', ',')
        self._setParam(params, dictionary, 'dictionary', ',')
        params['results'] = str(results)
        
        dom = self._getDOM(params)
        
        segmentlist = [
                       Segment(self._getText(s, 'SegmentText'),
                               self._getText(s, 'Alphanumeric'),
                               self._getText(s, 'HalfAlphanumeric'),
                               self._getText(s, 'Katakana'),
                               self._getText(s, 'HalfKatakana'),
                               self._getText(s, 'Hiragana'),
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


