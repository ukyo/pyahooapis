#coding: utf-8

from pyahooapis.service import Service, BaseObject


RESULT_MA = 'ma'
RESULT_UNIQ = 'uniq'


RESPONSE_SURFACE = 'surface'
RESPONSE_READING = 'reading'
RESPONSE_POS = 'pos'
RESPONSE_BASEFORM = 'baseform'
RESPONSE_FEATURE = 'feature'


FILTER_KEIYOUSHI = '1'
FILTER_KEIYOUDOUSHI = '2'
FILTER_KANDOUSHI = '3'
FILTER_FUKUSHI = '4'
FILTER_RENTAISHI = '5'
FILTER_SETSUZOKUSHI = '6'
FILTER_SETTOUJI = '7'
FILTER_SETSUBIJI = '8'
FILTER_MEISHI = '9'
FILTER_DOUSHI = '10'
FILTER_JOSHI = '11'
FILTER_JODOUSHI = '12'
FILTER_TOKUSHU = '13'


class MAService(Service):
    
    def __init__(self, appid):
        Service.__init__(self, appid, 'http://jlp.yahooapis.jp/MAService/V1/parse')
    
    def _get_result(self, results, kind, dom):
        r = dom.getElementsByTagName(kind)[0]
        return Result(self._getText(r, 'total_count'),
                      self._getText(r, 'filtered_count'),
                      [Word(self._getText(w, 'surface'),
                            self._getText(w, 'reading'),
                            self._getText(w, 'pos'),
                            self._getText(w, 'baseform'),
                            self._getText(w, 'feature'),
                            self._getText(w, 'count'))
                       for w in r.getElementsByTagName('word')])
    
    def get_result_set(self,
                     sentence,
                     results=[RESULT_MA],
                     response=(RESPONSE_SURFACE, RESPONSE_READING, RESPONSE_POS),
                     filter=None,
                     ma_response=None,
                     ma_filter=None,
                     uniq_response=None,
                     uniq_filter=None,
                     uniq_by_baseform=False,
                     json=False):
        '''
        詳しくは
        http://developer.yahoo.co.jp/webapi/jlp/ma/v1/parse.html
        
        Args:
            sentence: 解析する文章
            results: 解析結果の種類(listで指定してね)
            response: 解析結果の形態素情報(listかtuple)
            filter: 解析結果として出力する品詞(listかtuple)
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
        params['results'] = ','.join(results)
        params['response'] = ','.join(response)
        self._setParam(params, filter, 'filter', '|')
        self._setParam(params, ma_response, 'ma_response', ',')
        self._setParam(params, ma_filter, 'ma_filter', '|')
        self._setParam(params, uniq_response, 'uniq_response', ',')
        self._setParam(params, uniq_filter, 'uniq_filter', '|')
        params['uniq_by_baseform'] = str(uniq_by_baseform).lower()
        
        dom = self._getDOM(params)
        
        resultset = ResultSet()
        
        if results.count(RESULT_MA) > 0:
            resultset.ma_result = self._get_result(results, 'ma_result', dom)
        
        if results.count(RESULT_UNIQ) > 0:
            resultset.uniq_result = self._get_result(results, 'uniq_result', dom)
        
        return self.py2json(resultset) if json else resultset
    
    def get_ma_result(self,
                    sentence,
                    response=(RESPONSE_SURFACE, RESPONSE_READING, RESPONSE_POS),
                    filter=None,
                    json=False):
        if json:
            return self.get_result_set(sentence=sentence,
                                    response=response,
                                    filter=filter,
                                    json=json)
        else:
            return self.get_result_set(sentence=sentence,
                                    response=response,
                                    filter=filter,
                                    json=json).ma_result
    
    def get_uniq_result(self,
                      sentence,
                      response=(RESPONSE_SURFACE, RESPONSE_READING, RESPONSE_POS),
                      filter=None,
                      json=False):
        if json:
            return self.get_result_set(sentence=sentence,
                                    results=[RESULT_UNIQ],
                                    response=response,
                                    filter=filter,
                                    json=json)
        else:
            return self.get_result_set(sentence=sentence,
                                    results=[RESULT_UNIQ],
                                    response=response,
                                    filter=filter,
                                    json=json).uniq_result


class ResultSet(BaseObject):
    def __init__(self, ma_result=None, uniq_result=None):
        self.ma_result = ma_result
        self.uniq_result = uniq_result


class Result(BaseObject):
    def __init__(self,
                 total_count,
                 filtered_count,
                 words):
        self.total_count = total_count
        self.filtered_count = filtered_count
        self.words = words


class Word(BaseObject):
    def __init__(self,
                 surfase=None,
                 reading=None,
                 pos=None,
                 baseform=None,
                 feature=None,
                 count=None):
        self.surfase = surfase
        self.reading = reading
        self.pos = pos
        self.baseform = baseform
        self.feature = feature
        self.count = count
    
    def __str__(self):
        return self.surfase or self.reading or self.baseform or self.pos or self.feature

