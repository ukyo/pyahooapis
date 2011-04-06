#coding: utf-8

from pyahooapis.service import Service, BaseObject


JSON_ORIGINAL = "json"
JSON_LIBRALY = "json_lib"

class KeyphraseService(Service):
    def __init__(self, appid):
        Service.__init__(self, appid, "http://jlp.yahooapis.jp/KeyphraseService/V1/extract")
    
    def get_results(self, sentence, json=False):
        '''
        
        Args:
            sentence: 解析する文章
            json: JSON形式で返すかどうか(二種類あるよ)
        Returns:
            jsonがJSON_ORIGINALならYahoo!キーフレーズ抽出で提供されている
            オリジナルのJSON形式で返す。
            例:
                {"keyphrase1" : "100", "keyphrase2" : "75"}
            
            jsonがJSON_LIBRALYならこのライブラリーで生成したJSON形式で返す。
            例:
                [
                    {
                        "keyphrase" : "keyphrase1",
                        "score" : 100
                    },
                    {
                        "keyphrase" : "keyphrase2",
                        "score" : 75
                    }
                ]
            
            jsonがFalseならKeyphraseResultオブジェクトのリストを返す。
        '''
        
        params = {}
        
        params["sentence"] = sentence
        
        if json == JSON_ORIGINAL:
            params["output"] = JSON_ORIGINAL
            return self._response(params)
        else:
            params["output"] = "xml"
            dom = self._getDOM(params)
            resultlist = [
                          KeyphraseResult(self._getText(r, "Keyphrase"),
                                 self._getText(r, "Score"))
                          for r in dom.getElementsByTagName("Result")
                          ]
            
            return self.py2json(resultlist) if json == JSON_LIBRALY else resultlist

class KeyphraseResult(BaseObject):
    def __init__(self, keyphrase, score):
        self.keyphrase = keyphrase
        self.score = score

    def __str__(self):
        return self.keyphrase.encode('utf8')

