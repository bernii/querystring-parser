===================
querystring-parser
===================

This repository hosts the query string parser for Python/Django projects that correcly creates nested dictionaries from sent form/querystring data.

When to use it?
================

Lets say you have some textfields on your webpage that you wish to get as dictionary on the backend. The querystring could look like:
:: 
  section[1]['words'][2]=a&section[0]['words'][2]=a&section[0]['words'][2]=b

Standard django REQUEST (QueryDict) variable will contain:
::
  <QueryDict: {u"section[1]['words'][2]": [u'a'], u"section[0]['words'][2]": [u'a', u'b']}>

As you see it doesn't really convert it to dict. Instead of elegant dictionary you have a string called "section[1]['words'][2]" and "section[0]['words'][2]" and if you want to do something with it, you'll need to parse it (sic!).

When using querystring-parser the output will look like:
::
  {u'section': {0: {u'words': {2: [u'a', u'b']}}, 1: {u'words': {2: u'a'}}}}

Tadam! Everything is much simpler and more beautiful now :)

Efficiency:
============

Test made using timeit show that in most cases speed of created library is similar to standard Django QueryDict parsing speed. For query string containing multidimensional complicated arrays  querystring-parser is significantly slower. This is totally understandable as created library creates nested dictionaries in contrary to standard Django function which only tokenizes data. You can see results below.
Edit: Actually parsing is done by urlparse.parse_qs so I've added it to tests.

::

  Test string nr  querystring-parser     Django QueryDict       parse_qs
  0               4.82506012917          3.55248403549          0.624882936478
  Test string nr  querystring-parser     Django QueryDict       parse_qs
  1               18.0065619946          10.122371912           2.11287093163
  Test string nr  querystring-parser     Django QueryDict       parse_qs
  2               0.728802204132         1.23571300507          0.293427944183
  Test string nr  querystring-parser     Django QueryDict       parse_qs
  3               0.11042714119          0.462118148804         0.0700409412384
  Test string nr  querystring-parser     Django QueryDict       parse_qs
  4               0.00325989723206       0.171162128448         0.0170328617096


1* Is most interesting as is contains nested dictionaries in query string.

How to use:
============

Just add it to your Django project and start using it.  
::
  from querystring_parser import parser
  post_dict = parser.parse(request.POST.urlencode())

