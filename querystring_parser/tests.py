# coding: utf-8
'''
Created on 2011-05-13

@author: berni
'''

from parser import parse, MalformedQueryStringError
import unittest

#queryString ="packetname=fd&section[0]['words'][2]=&section[0]['words'][2]=&language=1&packetdesc=sdfsd&newlanguage=proponowany+jezyk..&newsectionname=&section[0]['words'][1]=&section[0]['words'][1]=&packettype=radio&section[0]['words'][0]=sdfsd&section[0]['words'][0]=ds"
# http://192.168.0.176:8000/packets/edit/4/Chemia%20spr?advInput=0&advInputTxtArea=sekcja%20siatkarska%0Anoga%20%7C%20leg%0A%0Asekcja%20siatkarska1%0Arenca%20%7C%20rukka%0Akciuk%20%7C%20thimb%0Aoko%20%7C%20an%20eye%0A%0Asekcja%20siatkarska2%0Awlos%20%7C%20a%20hair%0A%0A&language=1&newlanguage=proponowany%20jezyk..&newsectionname=&packetdesc=Zajebiste%20slowka%20na%20jutrzejszy%20sprawdzian%20z%20chemii&packetid=4&packetname=Chemia%20spr&packettype=1&section%5B10%5D%5B'name'%5D=sekcja%20siatkarska&section%5B10%5D%5B'words'%5D%5B-1%5D=&section%5B10%5D%5B'words'%5D%5B-1%5D=&section%5B10%5D%5B'words'%5D%5B-2%5D=&section%5B10%5D%5B'words'%5D%5B-2%5D=&section%5B10%5D%5B'words'%5D%5B30%5D=noga&section%5B10%5D%5B'words'%5D%5B30%5D=leg&section%5B11%5D%5B'del_words'%5D%5B32%5D=kciuk&section%5B11%5D%5B'del_words'%5D%5B32%5D=thimb&section%5B11%5D%5B'del_words'%5D%5B33%5D=oko&section%5B11%5D%5B'del_words'%5D%5B33%5D=an%20eye&section%5B11%5D%5B'name'%5D=sekcja%20siatkarska1&section%5B11%5D%5B'words'%5D%5B-1%5D=&section%5B11%5D%5B'words'%5D%5B-1%5D=&section%5B11%5D%5B'words'%5D%5B-2%5D=&section%5B11%5D%5B'words'%5D%5B-2%5D=&section%5B11%5D%5B'words'%5D%5B31%5D=renca&section%5B11%5D%5B'words'%5D%5B31%5D=rukka&section%5B12%5D%5B'name'%5D=sekcja%20siatkarska2&section%5B12%5D%5B'words'%5D%5B-1%5D=&section%5B12%5D%5B'words'%5D%5B-1%5D=&section%5B12%5D%5B'words'%5D%5B-2%5D=&section%5B12%5D%5B'words'%5D%5B-2%5D=&section%5B12%5D%5B'words'%5D%5B34%5D=wlos&section%5B12%5D%5B'words'%5D%5B34%5D=a%20hair&section%5B9%5D%5B'words'%5D%5B-1%5D=&section%5B9%5D%5B'words'%5D%5B-1%5D=&section%5B9%5D%5B'words'%5D%5B-2%5D=&section%5B9%5D%5B'words'%5D%5B-2%5D=&section%5B9%5D%5B'words'%5D%5B13397%5D=ko%C5%82omyjka&section%5B9%5D%5B'words'%5D%5B13397%5D=brisk%20Carpathian%20dance&section%5B9%5D%5B'words'%5D%5B13398%5D=tancbuda&section%5B9%5D%5B'words'%5D%5B13398%5D=dance%20hall&section%5B9%5D%5B'words'%5D%5B13399%5D=taniec%20ludowy&section%5B9%5D%5B'words'%5D%5B13399%5D=folk%20dance&section%5B9%5D%5B'words'%5D%5B13400%5D=taniec%20brzucha&section%5B9%5D%5B'words'%5D%5B13400%5D=belly%20dance&section%5B9%5D%5B'words'%5D%5B26%5D=leczyc&section%5B9%5D%5B'words'%5D%5B26%5D=treat&section%5B9%5D%5B'words'%5D%5B27%5D=wrzod&section%5B9%5D%5B'words'%5D%5B27%5D=costamer%20wrzudzik&section%5B9%5D%5B'words'%5D%5B28%5D=dupa&section%5B9%5D%5B'words'%5D%5B28%5D=ass&section%5B9%5D%5B'words'%5D%5B29%5D=glowa&section%5B9%5D%5B'words'%5D%5B29%5D=head&sectionnew%5B%5D=sekcja%20siatkarska&sectionnew%5B%5D=sekcja%20siatkarska1&sectionnew%5B%5D=sekcja%20siatkarska2&tags=dance%2C%20angielski%2C%20taniec


class KnownValues(unittest.TestCase):
    '''
    Test output for known query string values
    '''
    knownValuesClean = (
                    (
                     "packetname=fd&section[0]['words'][2]=&section[0]['words'][2]=&language=1&packetdesc=sdfsd&newlanguage=proponowany jezyk..&newsectionname=&section[0]['words'][1]=&section[0]['words'][1]=&packettype=radio&section[0]['words'][0]=sdfsd&section[0]['words'][0]=ds",
                     {"packetname": "fd", "section": {0: {"words": {0: ["sdfsd", "ds"], 1: ["", ""], 2: ["", ""]}}}, "language": 1, "packetdesc": "sdfsd", "newlanguage": "proponowany jezyk..", "newsectionname": "", "packettype": "radio"}
                     ),
                     (
                      "language=1&newlanguage=proponowany jezyk..&newsectionname=&packetdesc=Zajebiste slowka na jutrzejszy sprawdzian z chemii&packetid=4&packetname=Chemia spr&packettype=1&section[10]['name']=sekcja siatkarska&section[10]['words'][-1]=&section[10]['words'][-1]=&section[10]['words'][-2]=&section[10]['words'][-2]=&section[10]['words'][30]=noga&section[10]['words'][30]=leg&section[11]['del_words'][32]=kciuk&section[11]['del_words'][32]=thimb&section[11]['del_words'][33]=oko&section[11]['del_words'][33]=an eye&section[11]['name']=sekcja siatkarska1&section[11]['words'][-1]=&section[11]['words'][-1]=&section[11]['words'][-2]=&section[11]['words'][-2]=&section[11]['words'][31]=renca&section[11]['words'][31]=rukka&section[12]['name']=sekcja siatkarska2&section[12]['words'][-1]=&section[12]['words'][-1]=&section[12]['words'][-2]=&section[12]['words'][-2]=&section[12]['words'][34]=wlos&section[12]['words'][34]=a hair&sectionnew=sekcja siatkarska&sectionnew=sekcja siatkarska1&sectionnew=sekcja siatkarska2&tags=dance, angielski, taniec",
                      {"packetdesc": "Zajebiste slowka na jutrzejszy sprawdzian z chemii", "packetid": 4, "packetname": "Chemia spr",
                       "section": {10: {"words": {-1: ["", ""], -2: ["", ""], 30: ["noga", "leg"]}, "name": "sekcja siatkarska"},
                                  11: {"words": {-1: ["", ""], -2: ["", ""], 31: ["renca", "rukka"]},
                                      "del_words": {32: ["kciuk", "thimb"], 33: ["oko", "an eye"]},
                                      "name": "sekcja siatkarska1"},
                                  12: {"words": {-1: ["", ""], -2: ["", ""], 34: ["wlos", "a hair"]},
                                      "name": "sekcja siatkarska2"}},
                       "language": 1, "newlanguage": "proponowany jezyk..", "packettype": 1,
                       "tags": "dance, angielski, taniec", "newsectionname": "",
                       "sectionnew": ["sekcja siatkarska", "sekcja siatkarska1", "sekcja siatkarska2"]}
                      ),
                      (
                       "f=a hair&sectionnew[]=sekcja siatkarska&sectionnew[]=sekcja siatkarska1&sectionnew[]=sekcja siatkarska2",
                       {"f": "a hair", "sectionnew": {"": ["sekcja siatkarska", "sekcja siatkarska1", "sekcja siatkarska2"]}}
                       ),
                       ("f=a", {"f": "a"}),
                       ("", {}),
                       )

    knownValues = (
                    (
                     "packetname=f%26d&section%5B0%5D%5B%27words%27%5D%5B2%5D=&section%5B0%5D%5B%27words%27%5D%5B2%5D=&language=1&packetdesc=sdfsd&newlanguage=proponowany+jezyk..&newsectionname=&section%5B0%5D%5B%27words%27%5D%5B1%5D=&section%5B0%5D%5B%27words%27%5D%5B1%5D=&packettype=radio&section%5B0%5D%5B%27words%27%5D%5B0%5D=sdfsd&section%5B0%5D%5B%27words%27%5D%5B0%5D=ds",
                     {"packetname": "f&d", "section": {0: {"words": {0: ["sdfsd", "ds"], 1: ["", ""], 2: ["", ""]}}}, "language": 1, "packetdesc": "sdfsd", "newlanguage": "proponowany jezyk..", "newsectionname": "", "packettype": "radio"}
                     ),
                     (
                      "language=1&newlanguage=proponowany+jezyk..&newsectionname=&packetdesc=Zajebiste+slowka+na+jutrzejszy+sprawdzian+z+chemii&packetid=4&packetname=Chemia+spr&packettype=1&section%5B10%5D%5B%27name%27%5D=sekcja+siatkarska&section%5B10%5D%5B%27words%27%5D%5B-1%5D=&section%5B10%5D%5B%27words%27%5D%5B-1%5D=&section%5B10%5D%5B%27words%27%5D%5B-2%5D=&section%5B10%5D%5B%27words%27%5D%5B-2%5D=&section%5B10%5D%5B%27words%27%5D%5B30%5D=noga&section%5B10%5D%5B%27words%27%5D%5B30%5D=leg&section%5B11%5D%5B%27del_words%27%5D%5B32%5D=kciuk&section%5B11%5D%5B%27del_words%27%5D%5B32%5D=thimb&section%5B11%5D%5B%27del_words%27%5D%5B33%5D=oko&section%5B11%5D%5B%27del_words%27%5D%5B33%5D=an+eye&section%5B11%5D%5B%27name%27%5D=sekcja+siatkarska1&section%5B11%5D%5B%27words%27%5D%5B-1%5D=&section%5B11%5D%5B%27words%27%5D%5B-1%5D=&section%5B11%5D%5B%27words%27%5D%5B-2%5D=&section%5B11%5D%5B%27words%27%5D%5B-2%5D=&section%5B11%5D%5B%27words%27%5D%5B31%5D=renca&section%5B11%5D%5B%27words%27%5D%5B31%5D=rukka&section%5B12%5D%5B%27name%27%5D=sekcja+siatkarska2&section%5B12%5D%5B%27words%27%5D%5B-1%5D=&section%5B12%5D%5B%27words%27%5D%5B-1%5D=&section%5B12%5D%5B%27words%27%5D%5B-2%5D=&section%5B12%5D%5B%27words%27%5D%5B-2%5D=&section%5B12%5D%5B%27words%27%5D%5B34%5D=wlos&section%5B12%5D%5B%27words%27%5D%5B34%5D=a+hair&sectionnew=sekcja%3Dsiatkarska&sectionnew=sekcja+siatkarska1&sectionnew=sekcja+siatkarska2&tags=dance%2C+angielski%2C+taniec",
                      {"packetdesc": "Zajebiste slowka na jutrzejszy sprawdzian z chemii", "packetid": 4, "packetname": "Chemia spr",
                       "section": {10: {"words": {-1: ["", ""], -2: ["", ""], 30: ["noga", "leg"]}, "name": "sekcja siatkarska"},
                                  11: {"words": {-1: ["", ""], -2: ["", ""], 31: ["renca", "rukka"]},
                                      "del_words": {32: ["kciuk", "thimb"], 33: ["oko", "an eye"]},
                                      "name": "sekcja siatkarska1"},
                                  12: {"words": {-1: ["", ""], -2: ["", ""], 34: ["wlos", "a hair"]},
                                      "name": "sekcja siatkarska2"}},
                       "language": 1, "newlanguage": "proponowany jezyk..", "packettype": 1,
                       "tags": "dance, angielski, taniec", "newsectionname": "",
                       "sectionnew": ["sekcja=siatkarska", "sekcja siatkarska1", "sekcja siatkarska2"]}
                      ),
                      (
                       "f=a+hair&sectionnew%5B%5D=sekcja+siatkarska&sectionnew%5B%5D=sekcja+siatkarska1&sectionnew%5B%5D=sekcja+siatkarska2",
                       {"f": "a hair", "sectionnew": {"": ["sekcja siatkarska", "sekcja siatkarska1", "sekcja siatkarska2"]}}
                       ),
                       ("f=a", {"f": "a"}),
                       ("", {}),
                       )

    def test_parse_known_values_clean(self):
        """parse should give known result with known input"""
        for query_string, dic in self.knownValuesClean:
            result = parse(query_string, False)
            self.assertEqual(dic, result)

    def test_parse_known_values(self):
        """parse should give known result with known input (quoted)"""
        for query_string, dic in self.knownValues:
            result = parse(query_string)
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

if __name__ == "__main__":
    unittest.main()
