# coding: utf-8
'''
Created on 2011-05-12

@author: berni
'''

import re
entryName = re.compile('^[\w]+') # variable name
hasVariableName = re.compile('^[\w]+\[') # variable name before index
moreThanOneIndex = re.compile('\[.*\]\[.*\]') # does have more than one index (nested table)
getKey = re.compile("\['?([-\w]*)'?\]") # get key
isNumber= re.compile("^[-]?[\d]+$") # [-\d]+ # is it number
__DEBUG__ = False

#Define exceptions
class MalformedQueryStringError(Exception): pass       

def parserHelper(key, val):
    dict = {}
    if __DEBUG__ :
        print "%s = %s" % (key , val)     
    if hasVariableName.match(key) is not None: # var['key'][3]
        (start,end) = entryName.match(key).span()
        if __DEBUG__ :
            print "1 s:%s e:%s -> %s" % (start,end, key[start:end])
        dict[entryName.match(key).group()] = parserHelper(key[end:],val)
    elif moreThanOneIndex.match(key) is not None: # ['key'][3] 
        (start,end) = getKey.match(key).span()
        if __DEBUG__ :
            print "2 s:%s e:%s -> %s" % (start,end, key[start:end])
        newkey = getKey.match(key).groups()[0]
        if isNumber.match(newkey):
            newkey = eval(newkey)
        dict[newkey] = parserHelper(key[end:],val)
    elif key.find("[") != -1: # ['key'] 
        v_key = getKey.match(key)
        if v_key is None:
            raise MalformedQueryStringError
        (start,end) = v_key.span()
        if __DEBUG__ :
            print "4 s:%s e:%s -> %s" % (start,end, key[start:end])
        newkey = getKey.match(key).groups()[0]
        if __DEBUG__ :
            print newkey+" is digit ? "+str(newkey.isdigit())+" val: "+str(val)
        if isNumber.match(newkey):
            newkey = eval(newkey)
        if isNumber.match(val):
            val = eval(val)
        dict[newkey] = val
    else: # key = val
        newkey = key
        if isNumber.match(newkey):
            newkey = int(newkey)    
        if isNumber.match(val):
            val = int(val)    
        dict[newkey] = val
    return dict

def parse(queryString):
    mydict = {}
    list = []
    if __DEBUG__:
        print "Q: "+queryString
    if queryString == "":
        return mydict
    for element in queryString.split("&"):
        try:
            (var,val) = element.split("=")
        except ValueError:
            raise MalformedQueryStringError
        list.append(parserHelper(var,val))
    if __DEBUG__ :
        print "LIST BEFORE MERGE"
        print list
    for di in list:
        if __DEBUG__ :
            print "Di = "+str(di)+" Dict = " + str(mydict)
        (k,v) = di.popitem()
        if __DEBUG__ :
            print "Connecting  %s + %s " % (str(k),str(v))
        tempdict = mydict
        while k in tempdict and type(v) is dict : 
            tempdict = tempdict[k]
            (k,v) = v.popitem() 
        if k in tempdict and type(tempdict[k]).__name__=='list':
            tempdict[k].append(v)
        elif k in tempdict:
            tempdict[k] = [tempdict[k],v]
        else:
            tempdict[k] = v
    return mydict  


if __name__ == '__main__':
    """Compare speed with Django QueryDict"""
    from timeit import Timer
    from tests import KnownValues
    import os, sys
    from django.core.management import setup_environ
    # Add project dir so Djnago project settings is in the scope
    lib_path = os.path.abspath('..')
    sys.path.append(lib_path)
    import settings
    setup_environ(settings)
    
    i = 0
    for key,val in KnownValues.knownValues:
        statement = "parse(\"%s\")" % key
        statementd = "http.QueryDict(\"%s\")" % key
        t = Timer(statement, "from __main__ import parse")
        td = Timer(statementd, "from django import http")
        print "Test string nr ".ljust(15),  " querystring-parser".ljust(22), "Django QueryDict"
        print str(i).ljust(15),  str(min(t.repeat(3,1000))).ljust(22), min(td.repeat(3,1000))
        i+=1