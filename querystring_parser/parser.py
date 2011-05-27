# coding: utf-8
'''
Created on 2011-05-12

@author: berni
'''

import re
import urllib
ENTRY_NAME = re.compile('^[\w]+') # variable name
HAS_VARIABLE_NAME = re.compile('^[\w]+\[') # variable name before index
MORE_THAN_ONE_INDEX = re.compile('\[.*\]\[.*\]') # does have more than one index (nested table)
GET_KEY = re.compile("\['?([-\w]*)'?\]") # get key
IS_NUMBER = re.compile("^[-]?[\d]+$") # [-\d]+ # is it number
__DEBUG__ = False


class MalformedQueryStringError(Exception):
    '''
    Query string is malformed, can't parse it :(
    '''
    pass


def parser_helper(key, val):
    '''
    Helper for parser function
    @param key:
    @param val:
    '''
    pdict = {}
    if __DEBUG__:
        print "%s = %s" % (key, val)
    if HAS_VARIABLE_NAME.match(key) is not None: # var['key'][3]
        (start, end) = ENTRY_NAME.match(key).span()
        if __DEBUG__:
            print "1 s:%s e:%s -> %s" % (start, end, key[start:end])
        pdict[ENTRY_NAME.match(key).group()] = parser_helper(key[end:], val)
    elif MORE_THAN_ONE_INDEX.match(key) is not None: # ['key'][3]
        (start, end) = GET_KEY.match(key).span()
        if __DEBUG__:
            print "2 s:%s e:%s -> %s" % (start, end, key[start:end])
        newkey = GET_KEY.match(key).groups()[0]
        if IS_NUMBER.match(newkey):
            newkey = eval(newkey)
        pdict[newkey] = parser_helper(key[end:], val)
    elif key.find("[") != -1: # ['key']
        v_key = GET_KEY.match(key)
        if v_key is None:
            raise MalformedQueryStringError
        (start, end) = v_key.span()
        if __DEBUG__:
            print "4 s:%s e:%s -> %s" % (start, end, key[start:end])
        newkey = GET_KEY.match(key).groups()[0]
        if __DEBUG__:
            print newkey + " is digit ? " + str(newkey.isdigit()) + " val: " + str(val)
        if IS_NUMBER.match(newkey):
            newkey = eval(newkey)
        if IS_NUMBER.match(val):
            val = eval(val)
        pdict[newkey] = val
    else: # key = val
        newkey = key
        if IS_NUMBER.match(newkey):
            newkey = int(newkey)
        if IS_NUMBER.match(val):
            val = int(val)
        pdict[newkey] = val
    return pdict


def parse(query_string, unquote=True):
    '''
    Main parse function
    @param query_string:
    @param unquote: unquote html query string ?
    '''
    mydict = {}
    plist = []
    if __DEBUG__:
        print "Q: " + query_string
    if query_string == "":
        return mydict
    for element in query_string.split("&"):
        try:
            if unquote:
                (var, val) = element.split("=")
                var = urllib.unquote_plus(var)
                val = urllib.unquote_plus(val)
            else:
                (var, val) = element.split("=")
        except ValueError:
            raise MalformedQueryStringError
        plist.append(parser_helper(var, val))
    if __DEBUG__:
        print "LIST BEFORE MERGE"
        print plist
    for di in plist:
        if __DEBUG__:
            print "Di = " + str(di) + " Dict = " + str(mydict)
        (k, v) = di.popitem()
        if __DEBUG__:
            print "Connecting  %s + %s " % (str(k), str(v))
        tempdict = mydict
        while k in tempdict and type(v) is dict:
            tempdict = tempdict[k]
            (k, v) = v.popitem()
        if k in tempdict and type(tempdict[k]).__name__ == 'list':
            tempdict[k].append(v)
        elif k in tempdict:
            tempdict[k] = [tempdict[k], v]
        else:
            tempdict[k] = v
    return mydict


if __name__ == '__main__':
    """Compare speed with Django QueryDict"""
    from timeit import Timer
    from tests import KnownValues
    import os
    import sys
    from django.core.management import setup_environ
    # Add project dir so Djnago project settings is in the scope
    LIB_PATH = os.path.abspath('..')
    sys.path.append(LIB_PATH)
    import settings
    setup_environ(settings)

    i = 0
    for key, val in KnownValues.knownValues:
        statement = "parse(\"%s\")" % key
        statementd = "http.QueryDict(\"%s\")" % key
        statementqs = "parse_qs(\"%s\")" % key
        t = Timer(statement, "from __main__ import parse")
        td = Timer(statementd, "from django import http")
        tqs = Timer(statementqs, "from urlparse import parse_qs")
        print "Test string nr ".ljust(15), "querystring-parser".ljust(22), "Django QueryDict".ljust(22), "parse_qs"
        print str(i).ljust(15), str(min(t.repeat(3, 10000))).ljust(22), str(min(td.repeat(3, 10000))).ljust(22), min(tqs.repeat(3, 10000))
        i += 1
