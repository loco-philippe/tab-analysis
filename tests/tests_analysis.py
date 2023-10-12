# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 23:06:12 2023

@author: philippe@loco-labs.io
"""
import unittest
from pprint import pprint
from tab_analysis import AnaField, AnaRelation

class Test_AnaField_AnaRelation(unittest.TestCase):
    
    def test_creation(self):
        fld1 = AnaField('var1', 10, 5, 20)
        fld2 = AnaField('var2', 100, 50, 200)
        rel1 = AnaRelation(['var1', 'var2'], 200)    
        self.assertEqual(rel1.to_dict(relation=True), {'dist': 200, 'relation': ['var1', 'var2']})
        self.assertEqual(rel1.to_dict(relation=True, distance=True), 
                         {'dist': 200, 'relation': ['var1', 'var2'],
                          'distance': 190, 'distomin': 100, 'distomax': 800,
                          'ratecpl': 0.1919191919191919, 'rateder': 0.1111111111111111})
        
if __name__ == '__main__':
    
    unittest.main(verbosity=2)
