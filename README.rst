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

::

  Test string nr   querystring-parser    Django QueryDict
  0               0.357883930206         0.308471918106
  Test string nr   querystring-parser    Django QueryDict
  1*              1.39680719376          0.900585889816
  Test string nr   querystring-parser    Django QueryDict
  2               0.0441470146179        0.11444401741
  Test string nr   querystring-parser    Django QueryDict
  3               0.00601196289062       0.0453128814697
  Test string nr   querystring-parser    Django QueryDict
  4               0.000290870666504      0.0167441368103

1* Is most interesting as is contains nested dictionaries in query string.

How to use:
============

Just add it to your Django project and start using it.  
::
  from querystring_parser import parser
  post_dict = parser.parse(urllib.unquote_plus(request.POST.urlencode()))

