# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 23:06:12 2023

@author: philippe@loco-labs.io
"""
import unittest
from pprint import pprint
from tab_analysis import AnaField, AnaRelation, AnaDataset

class Test_AnaField_AnaRelation(unittest.TestCase):
    
    def test_creation(self):
        fld1 = AnaField('var1', 10, 5, 20)
        fld2 = AnaField('var2', 100, 50, 200)
        fld3 = AnaField('var3', 500)
        self.assertEqual(fld1.to_dict(idfield=True), 
                         {'lencodec': 10, 'mincodec': 5, 'maxcodec': 20, 'id': 'var1'})
        self.assertEqual(fld1.to_dict(full=True), 
                         {'lencodec': 10, 'mincodec': 5, 'maxcodec': 20, 'id': 'var1',
                          'ratecodec': 0.6666666666666666, 'dmincodec': 5,
                          'dmaxcodec': 10, 'rancodec': 15})        
        rel1 = AnaRelation([fld1, fld2], 200)    
        self.assertEqual(rel1.to_dict(relation=True), {'dist': 200, 'relation': ['var1', 'var2']})
        self.assertEqual(rel1.to_dict(relation=True, distance=True), 
                         {'dist': 200, 'relation': ['var1', 'var2'],
                          'distance': 190, 'distomin': 100, 'distomax': 800,
                          'ratecpl': 0.1919191919191919, 'rateder': 0.1111111111111111})
        dts = AnaDataset([fld1, fld2, fld3])   
        dts.set_relations(fld1, {fld2: 12, fld3: 13})
        dts.set_relations(fld2, {fld3: 23})
        #print(dts.relations[fld1][fld2], dts.relations[fld2][fld1])
        self.assertTrue(dts.relations[fld1][fld2].dist == dts.relations[fld2][fld1].dist == 12)
        self.assertTrue(dts.relations[fld1][fld3].dist == dts.relations[fld3][fld1].dist == 13)
        
if __name__ == '__main__':
    
    unittest.main(verbosity=2)
