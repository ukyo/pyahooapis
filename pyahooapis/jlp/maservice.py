#coding: utf-8

from pyahooapis.service import Service, BaseObject


RESULT_MA = 1
RESULT_UNIQ = 2

RESULTS = {
    RESULT_MA : 'ma',
    RESULT_UNIQ : 'uniq'
    }

RESPONSE_SURFACE = 1
RESPONSE_READING = 2
RESPONSE_POS = 4
RESPONSE_BASEFORM = 8
RESPONSE_FEATURE = 16

RESPONSES = {
    RESPONSE_SURFACE : 'surface',
    RESPONSE_READING : 'reading',
    RESPONSE_POS : 'pos',
    RESPONSE_BASEFORM : 'baseform',
    RESPONSE_FEATURE : 'feature'
    }

FILTER_KEIYOUSHI = 1
FILTER_KEIYOUDOUSHI = 2
FILTER_KANDOUSHI = 4
FILTER_FUKUSHI = 8
FILTER_RENTAISHI = 16
FILTER_SETSUZOKUSHI = 32
FILTER_SETTOUJI = 64
FILTER_SETSUBIJI = 128
FILTER_MEISHI = 256
FILTER_DOUSHI = 512
FILTER_JOSHI = 1024
FILTER_JODOUSHI = 2048
FILTER_TOKUSHU = 4096

FILTERS = {
    FILTER_KEIYOUSHI : '1',
    FILTER_KEIYOUDOUSHI : '2',
    FILTER_KANDOUSHI : '3',
    FILTER_FUKUSHI : '4',
    FILTER_RENTAISHI : '5',
    FILTER_SETSUZOKUSHI : '6',
    FILTER_SETTOUJI : '7',
    FILTER_SETSUBIJI : '8',
    FILTER_MEISHI : '9',
    FILTER_DOUSHI : '10',
    FILTER_JOSHI : '11',
    FILTER_JODOUSHI : '12',
    FILTER_TOKUSHU : '13'
    }

class MAService(Service):
    url = 'http://jlp.yahooapis.jp/MAService/V1/parse'
    
    def _get_result(self, results, kind, dom):
        r = dom.getElementsByTagName(kind)[0]
        return Result(self._get_text(r, 'total_count'),
                      self._get_text(r, 'filtered_count'),
                      [Word(self._get_text(w, 'surface'),
                            self._get_text(w, 'reading'),
                            self._get_text(w, 'pos'),
                            self._get_text(w, 'baseform'),
                            self._get_text(w, 'feature'),
                            self._get_text(w, 'count'))
                       for w in r.getElementsByTagName('word')])
        
    def get_result_set(self, sentence, results=RESULT_MA, response=None, filter=None,
                       ma_response=None, ma_filter=None, uniq_response=None,
                       uniq_filter=None, uniq_by_baseform=False, json=False):
        '''
        詳しくは
        http://developer.yahoo.co.jp/webapi/jlp/ma/v1/parse.html
        
        Args:
            sentence: 解析する文章
            results: 解析結果の種類
            response: 解析結果の形態素情報
            filter: 解析結果として出力する品詞
            ma_response: ma側だけのresponse設定
            ma_filter: ma側だけのfilter設定
            uniq_response: uniq側だけのresponse設定
            uniq_filter: uniq側だけのfilter設定
            uniq_by_baseform: uniqで帰ってくる結果を基本形でまとめるかどうか
            json: JOSN形式で返すかどうか
        Returns:
            そのうち書く
        '''
        params = {}
        
        params['sentence'] = sentence
        if results is not None:
            params['results'] = self._binary2param(',', results, RESULTS)
        if response is not None:
            params['response'] = self._binary2param(',', response, RESPONSES)
        if filter is not None:
            params['filter'] = self._binary2param('|', filter, FILTERS)
        if ma_response is not None:
            params['ma_response'] = self._binary2param(',', ma_response, RESPONSES)
        if ma_filter is not None:
            params['ma_filter'] = self._binary2param('|', ma_filter, FILTERS)
        if uniq_response is not None:
            params['uniq_response'] = self._binary2param(',', uniq_response, RESPONSES)
        if uniq_filter is not None:
            params['uniq_filter'] = self._binary2param('|', uniq_response, FILTERS)
        if uniq_by_baseform is not False:
            params['uniq_by_baseform'] = str(uniq_by_baseform).lower()
        
        dom = self._get_dom(params)
        
        resultset = ResultSet()
        
        if results&RESULT_MA:
            resultset.ma_result = self._get_result(results, 'ma_result', dom)
        
        if results&RESULT_UNIQ:
            resultset.uniq_result = self._get_result(results, 'uniq_result', dom)
        
        return self.py2json(resultset) if json else resultset
    
    def get_ma_result(self, sentence, response=None, filter=None, json=False):
        if json:
            return self.get_result_set(sentence=sentence, response=response, filter=filter, json=json)
        else:
            return self.get_result_set(sentence=sentence, response=response, filter=filter, json=json).ma_result
    
    def get_uniq_result(self, sentence, response=None, filter=None, json=False):
        if json:
            return self.get_result_set(sentence=sentence, results=RESULT_UNIQ, response=response, filter=filter, json=json)
        else:
            return self.get_result_set(sentence=sentence, results=RESULT_UNIQ, response=response, filter=filter, json=json).uniq_result


class ResultSet(BaseObject):
    def __init__(self, ma_result=None, uniq_result=None):
        self.ma_result = ma_result
        self.uniq_result = uniq_result


class Result(BaseObject):
    def __init__(self, total_count, filtered_count, words):
        self.total_count = total_count
        self.filtered_count = filtered_count
        self.words = words


class Word(BaseObject):
    def __init__(self, surface=None, reading=None, pos=None, baseform=None, feature=None, count=None):
        self.surface = surface
        self.reading = reading
        self.pos = pos
        self.baseform = baseform
        self.feature = feature
        self.count = count
    
    def __str__(self):
        return self.encode(self.surface or self.reading or self.baseform or self.pos or self.feature)
