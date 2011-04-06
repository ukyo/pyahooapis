#coding: utf-8

from pyahooapis.service import Service, BaseObject


class DAService(Service):
    '''Yahoo!テキスト解析 日本語係り受け解析APIのPythonラッパー
    
    Example:
    >>> da = DAService(you're appid)
    
    >>> chunks = da.get_chunks('うちの庭には二羽鶏がいます。')
    >>> for chunk in chunks:
            print chunk, "->", chunks[chunk.dependency] if chunk.dependency != -1 else None
    
    うちの -> 庭には
    庭には -> います。
    二羽鶏が -> います。
    います。 -> None
    '''
    
    def __init__(self, appid):
        Service.__init__(self, appid, 'http://jlp.yahooapis.jp/DAService/V1/parse')
    
    def get_chunks(self, sentence, json=False):
        '''文節のリストを返す
        
        Args:
            sentence: 解析する文章
            json: JSON形式で返すかどうか
        Returns:
            もしjsonがTrueならJSON形式で値を返す。
            FalseならChunkオブジェクトのリストを返す。
        '''
        
        params = {'sentence' : sentence}
        dom = self._getDOM(params)
        
        chunks = []
        
        for c in dom.getElementsByTagName('Chunk'):
            morphems = [
                Morphem(self._getText(m, 'Surface'),
                        self._getText(m, 'Reading'),
                        self._getText(m, 'Baseform'),
                        self._getText(m, 'POS'),
                        self._getText(m, 'Feature'))
                for m in c.getElementsByTagName('Morphem')
            ]
            chunks.append(Chunk(int(self._getText(c, 'Id')),
                                   int(self._getText(c, 'Dependency')),
                                   morphems))
        
        return self.py2json(chunks) if json else chunks


class Chunk(BaseObject):
    '''文節の情報を含むクラス
    
    Properties:
        id: 文節の番号
        dependency: 装飾するid
        morphems: 形態素情報のリスト
    '''
    
    def __init__(self, id, dependency, morphems):
        self.id = id
        self.dependency = dependency
        self.morphems = morphems
    
    def __str__(self):
        return ''.join(morphem.surface for morphem in self.morphems).encode('utf8')


class Morphem(BaseObject):
    '''形態素の情報を含むクラス
    
    Properties:
        surface: 形態素の表記
        reading: 形態素の読みがな
        baseform: 形態素の基本形表記
        pos: 形態素の品詞
        feature: 形態素の全情報の文字列
    '''
    
    def __init__(self, surface, reading, baseform, pos, feature):
        self.surface = surface
        self.reading = reading
        self.baseform = baseform
        self.pos = pos
        self.feature = feature
    
    def __str__(self):
        return self.surface

