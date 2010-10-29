import daservice, furiganaservice, jimservice, keyphraseservice, kouseiservice, maservice


class JLPAPIs(object):
    
    def __init__(self, appid):
        self.da = daservice.DAService(appid)
        self.furigana = furiganaservice.FuriganaService(appid)
        self.jim = jimservice.JIMService(appid)
        self.keyphrase = keyphraseservice.KeyphraseService(appid)
        self.kousei = kouseiservice.KouseiService(appid)
        self.ma = maservice.MAService(appid)

