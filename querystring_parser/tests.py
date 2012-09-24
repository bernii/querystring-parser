# coding: utf-8
'''
Created on 2011-05-13

@author: berni

Updated 2012-03-28 Tomasz 'Doppler' Najdek
Updated 2012-09-24 Bernard 'berni' Kobos
'''

from parser import parse, MalformedQueryStringError
from builder import build
import unittest


class KnownValues(unittest.TestCase):
    '''
    Test output for known query string values
    '''
    knownValuesClean = (
                    (
                     # "packetname=fd&section[0]['words'][2]=&section[0]['words'][2]=&language=1&packetdesc=sdfsd&newlanguage=proponowany jezyk..&newsectionname=&section[0]['words'][1]=&section[0]['words'][1]=&packettype=radio&section[0]['words'][0]=sdfsd&section[0]['words'][0]=ds",
                     {u"packetname": u"fd", u"section": {0: {u"words": {0: [u"sdfsd", u"ds"], 1: [u"", u""], 2: [u"", u""]}}}, u"language": 1, u"packetdesc": u"sdfsd", u"newlanguage": u"proponowany jezyk..", u"newsectionname": u"", u"packettype": u"radio"}
                     ),
                     (
                      # "language=1&newlanguage=proponowany jezyk..&newsectionname=&packetdesc=Zajebiste slowka na jutrzejszy sprawdzian z chemii&packetid=4&packetname=Chemia spr&packettype=1&section[10]['name']=sekcja siatkarska&section[10]['words'][-1]=&section[10]['words'][-1]=&section[10]['words'][-2]=&section[10]['words'][-2]=&section[10]['words'][30]=noga&section[10]['words'][30]=leg&section[11]['del_words'][32]=kciuk&section[11]['del_words'][32]=thimb&section[11]['del_words'][33]=oko&section[11]['del_words'][33]=an eye&section[11]['name']=sekcja siatkarska1&section[11]['words'][-1]=&section[11]['words'][-1]=&section[11]['words'][-2]=&section[11]['words'][-2]=&section[11]['words'][31]=renca&section[11]['words'][31]=rukka&section[12]['name']=sekcja siatkarska2&section[12]['words'][-1]=&section[12]['words'][-1]=&section[12]['words'][-2]=&section[12]['words'][-2]=&section[12]['words'][34]=wlos&section[12]['words'][34]=a hair&sectionnew=sekcja siatkarska&sectionnew=sekcja siatkarska1&sectionnew=sekcja siatkarska2&tags=dance, angielski, taniec",
                      {u"packetdesc": u"Zajebiste slowka na jutrzejszy sprawdzian z chemii", u"packetid": 4, u"packetname": u"Chemia spr",
                       u"section": {10: {u"words": {-1: [u"", u""], -2: [u"", u""], 30: [u"noga", u"leg"]}, u"name": u"sekcja siatkarska"},
                                  11: {u"words": {-1: [u"", u""], -2: [u"", u""], 31: [u"renca", u"rukka"]},
                                      u"del_words": {32: [u"kciuk", u"thimb"], 33: [u"oko", u"an eye"]},
                                      u"name": u"sekcja siatkarska1"},
                                  12: {u"words": {-1: [u"", u""], -2: [u"", u""], 34: [u"wlos", u"a hair"]},
                                      u"name": u"sekcja siatkarska2"}},
                       u"language": 1, u"newlanguage": u"proponowany jezyk..", u"packettype": 1,
                       u"tags": u"dance, angielski, taniec", u"newsectionname": u"",
                       u"sectionnew": [u"sekcja siatkarska", u"sekcja siatkarska1", u"sekcja siatkarska2"]}
                      ),
                      (
                       # "f=a hair&sectionnew[]=sekcja siatkarska&sectionnew[]=sekcja siatkarska1&sectionnew[]=sekcja siatkarska2",
                       {u"f": u"a hair", u"sectionnew": {u"": [u"sekcja siatkarska", u"sekcja siatkarska1", u"sekcja siatkarska2"]}}
                       ),
                       # f = a
                       ({u"f": u"a"}),
                       # ""
                       ({}),
                       )

    knownValues = (
                    (
                     # "packetname=f%26d&section%5B0%5D%5B%27words%27%5D%5B2%5D=&section%5B0%5D%5B%27words%27%5D%5B2%5D=&language=1&packetdesc=sdfsd&newlanguage=proponowany+jezyk..&newsectionname=&section%5B0%5D%5B%27words%27%5D%5B1%5D=&section%5B0%5D%5B%27words%27%5D%5B1%5D=&packettype=radio&section%5B0%5D%5B%27words%27%5D%5B0%5D=sdfsd&section%5B0%5D%5B%27words%27%5D%5B0%5D=ds",
                     {u"packetname": u"f&d", u"section": {0: {u"words": {0: [u"sdfsd", u"ds"], 1: [u"", u""], 2: [u"", u""]}}}, u"language": 1, u"packetdesc": u"sdfsd", u"newlanguage": u"proponowany jezyk..", u"newsectionname": u"", u"packettype": u"radio"}
                     ),
                     (
                      # "language=1&newlanguage=proponowany+jezyk..&newsectionname=&packetdesc=Zajebiste+slowka+na+jutrzejszy+sprawdzian+z+chemii&packetid=4&packetname=Chemia+spr&packettype=1&section%5B10%5D%5B%27name%27%5D=sekcja+siatkarska&section%5B10%5D%5B%27words%27%5D%5B-1%5D=&section%5B10%5D%5B%27words%27%5D%5B-1%5D=&section%5B10%5D%5B%27words%27%5D%5B-2%5D=&section%5B10%5D%5B%27words%27%5D%5B-2%5D=&section%5B10%5D%5B%27words%27%5D%5B30%5D=noga&section%5B10%5D%5B%27words%27%5D%5B30%5D=leg&section%5B11%5D%5B%27del_words%27%5D%5B32%5D=kciuk&section%5B11%5D%5B%27del_words%27%5D%5B32%5D=thimb&section%5B11%5D%5B%27del_words%27%5D%5B33%5D=oko&section%5B11%5D%5B%27del_words%27%5D%5B33%5D=an+eye&section%5B11%5D%5B%27name%27%5D=sekcja+siatkarska1&section%5B11%5D%5B%27words%27%5D%5B-1%5D=&section%5B11%5D%5B%27words%27%5D%5B-1%5D=&section%5B11%5D%5B%27words%27%5D%5B-2%5D=&section%5B11%5D%5B%27words%27%5D%5B-2%5D=&section%5B11%5D%5B%27words%27%5D%5B31%5D=renca&section%5B11%5D%5B%27words%27%5D%5B31%5D=rukka&section%5B12%5D%5B%27name%27%5D=sekcja+siatkarska2&section%5B12%5D%5B%27words%27%5D%5B-1%5D=&section%5B12%5D%5B%27words%27%5D%5B-1%5D=&section%5B12%5D%5B%27words%27%5D%5B-2%5D=&section%5B12%5D%5B%27words%27%5D%5B-2%5D=&section%5B12%5D%5B%27words%27%5D%5B34%5D=wlos&section%5B12%5D%5B%27words%27%5D%5B34%5D=a+hair&sectionnew=sekcja%3Dsiatkarska&sectionnew=sekcja+siatkarska1&sectionnew=sekcja+siatkarska2&tags=dance%2C+angielski%2C+taniec",
                      {u"packetdesc": u"Zajebiste slowka na jutrzejszy sprawdzian z chemii", u"packetid": 4, u"packetname": u"Chemia spr",
                       u"section": {10: {u"words": {-1: [u"", u""], -2: [u"", u""], 30: [u"noga", u"leg"]}, u"name": u"sekcja siatkarska"},
                                  11: {u"words": {-1: [u"", u""], -2: [u"", u""], 31: [u"renca", u"rukka"]},
                                      u"del_words": {32: [u"kciuk", u"thimb"], 33: [u"oko", u"an eye"]},
                                      u"name": u"sekcja siatkarska1"},
                                  12: {u"words": {-1: [u"", u""], -2: [u"", u""], 34: [u"wlos", u"a hair"]},
                                      u"name": u"sekcja siatkarska2"}},
                       u"language": 1, u"newlanguage": u"proponowany jezyk..", u"packettype": 1,
                       u"tags": u"dance, angielski, taniec", u"newsectionname": "",
                       u"sectionnew": [u"sekcja=siatkarska", u"sekcja siatkarska1", u"sekcja siatkarska2"]}
                      ),
                      (
                       # "f=a+hair&sectionnew%5B%5D=sekcja+siatkarska&sectionnew%5B%5D=sekcja+siatkarska1&sectionnew%5B%5D=sekcja+siatkarska2",
                       {u"f": u"a hair", u"sectionnew": {u"": [u"sekcja siatkarska", u"sekcja siatkarska1", u"sekcja siatkarska2"]}}
                       ),
                       # f = a
                       ({u"f": u"a"}),
                       # ""
                       ({}),
                       )

    def test_parse_known_values_clean(self):
        """parse should give known result with known input"""
        self.maxDiff = None
        for dic in self.knownValuesClean:
            result = parse(build(dic), True)
            self.assertEqual(dic, result)

    def test_parse_known_values(self):
        """parse should give known result with known input (quoted)"""
        self.maxDiff = None
        for dic in self.knownValues:
            result = parse(build(dic))
            self.assertEqual(dic, result)


class ParseBadInput(unittest.TestCase):
    '''
    Test for exceptions when bad input is provided
    '''
    badQueryStrings = (
                        "f&a hair&sectionnew[]=sekcja siatkarska&sectionnew[]=sekcja siatkarska1&sectionnew[]=sekcja siatkarska2",
                        "f=a hair&sectionnew[=sekcja siatkarska&sectionnew[]=sekcja siatkarska1&sectionnew[]=sekcja siatkarska2",
                        "packetname==fd&newsectionname=",
                        "packetname=fd&newsectionname=&section[0]['words'][1",
                        "packetname=fd&newsectionname=&",
                       )

    def test_bad_input(self):
        """parse should fail with malformed querystring"""
        for qstr in self.badQueryStrings:
            self.assertRaises(MalformedQueryStringError, parse, qstr, False)


class BuildUrl(unittest.TestCase):
    '''
    Basic test to verify builder's functionality
    '''
    request_data = {
      u"word": u"easy",
      u"more_words": [u"medium", u"average"],
      u"words_with_translation": {u"hard": u"trudny", u"tough": u"twardy"},
      u"words_nested": {u"hard": [u"trudny", u"twardy"]}
    }

    known_result = 'words_with_translation[hard]=trudny&words_with_translation[tough]=twardy&words_nested[hard]=trudny&words_nested[hard]=twardy&word=easy&more_words=medium&more_words=average'

    def test_build(self):
        result = build(self.request_data)
        self.assertEquals(result, self.known_result)

    def test_end_to_end(self):
        self.maxDiff = None
        querystring = build(self.request_data)
        result = parse(querystring)
        self.assertEquals(result, self.request_data)


class BuilderAndParser(unittest.TestCase):
    '''
    Testing both builder and parser
    '''
    def test_end_to_end(self):
        parsed = parse('a[]=1&a[]=2')
        result = build(parsed)
        self.assertEquals(result, "a[]=1&a[]=2")

if __name__ == "__main__":
    unittest.main()
