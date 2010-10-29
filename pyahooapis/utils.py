#coding: utf-8

def import_json():
    try:
        '''Python 2.6 or later'''
        import json
        return json
    except:
        try:
            '''simplejson'''
            import simplejson
            return simplejson
        except:
            '''Google App Engine'''
            import django.utils.simplejson
            return django.utils.simplejson
