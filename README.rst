===================
querystring-parser ![Continuous Integration status](https://secure.travis-ci.org/bernii/querystring-parser.png)
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
  0               2.75077319145          3.44334220886          0.582501888275
  Test string nr  querystring-parser     Django QueryDict       parse_qs
  1               10.1889920235          10.2983090878          2.08930182457
  Test string nr  querystring-parser     Django QueryDict       parse_qs
  2               0.613747119904         1.21649289131          0.283004999161
  Test string nr  querystring-parser     Django QueryDict       parse_qs
  3               0.107316017151         0.459388017654         0.0687718391418
  Test string nr  querystring-parser     Django QueryDict       parse_qs
  4               0.00291299819946       0.169251918793         0.0170118808746


Test #1 Is most interesting as is contains nested dictionaries in query string.

How to use:
============

Just add it to your Django project and start using it.  
::
  from querystring_parser import parser
  post_dict = parser.parse(request.POST.urlencode())

