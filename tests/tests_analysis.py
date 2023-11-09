# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 23:06:12 2023

@author: philippe@loco-labs.io
"""
import unittest
#from pprint import pprint
from tab_analysis import AnaField, AnaRelation, AnaDataset, AnaDfield
from tab_analysis import ROOT, ROOTED, DERIVED, COUPLED
from tab_analysis import NULL, UNIQUE, COMPLETE, FULL, DEFAULT, MIXED
from observation.cdataset import Cdataset
from observation.cfield import Cfield
from observation import Sdataset

"""
il = Dataset.ntv([[1, 2, 3, 4, 5, 6],               root coupled
                  ['a', 'b', 'b', 'c', 'c', 'a'],   mixed
                  [20, 10, 10, 10, 10, 20],         derived from 1
                  [200, 200, 300, 200, 300, 300]])  derived from root
"""
i0 = AnaField('i0', 6, 6, 6)
i1 = AnaField('i1', 3, 3, 6)
i2 = AnaField('i2', 2, 2, 6)
i3 = AnaField('i3', 2, 2, 6)
i4 = AnaField('i4', 2, 2, 6)

i2i0 = AnaRelation([i2, i0], 6)
i2i1 = AnaRelation([i2, i1], 3)
i2i2 = AnaRelation([i2, i2], 2)
i2i3 = AnaRelation([i2, i3], 4)

dts = AnaDataset([i0, i1, i2, i3, i4], iddataset='test')   
dts.set_relations(i0, {i1: 6, i2: 6, i3: 6, i4: 6})
dts.set_relations(i1, {i0: 6, i2: 3, i3: 6, i4: 6})
dts.set_relations(i2, {i0: 6, i1: 3, i3: 4, i4: 4})
dts.set_relations(i3, {i0: 6, i1: 6, i2: 4, i4: 2})
dts.set_relations(i4, {i0: 6, i1: 6, i2: 4, i3: 2})

dic =   {'name': 'test', 'length': 6,
         'fields': [ 
            {'id': 'i0', 'lencodec': 6, 'mincodec': 6 },
            {'id': 'i1', 'lencodec': 3, 'mincodec': 3 },
            {'id': 'i2', 'lencodec': 2, 'mincodec': 2 },
            {'id': 'i3', 'lencodec': 2, 'mincodec': 2 },
            {'id': 'i4', 'lencodec': 2, 'mincodec': 2 }
            ],
         'relations': {'i0': {'i1': 6, 'i2': 6, 'i3': 6, 'i4': 6}, 
                       'i1': {'i2': 3, 'i3': 6, 'i4': 6},
                       'i2': {'i3': 4, 'i4': 4},
                       'i3': {'i4': 2}}
        }
class Test_Cdataset(unittest.TestCase):
    
    def test_dict(self):
        cdts = Cdataset(
            [Cfield([1, 2, 3, 4, 5, 6], 'i0', default=True),              #root coupled
             Cfield(['a', 'b', 'b', 'c', 'c', 'a'], 'i1', default=True),  #mixed
             Cfield([20, 10, 10, 10, 10, 20], 'i2', default=True),        #derived from 1
             Cfield([200, 200, 300, 200, 300, 300],  'i3', default=True), #derived from root
             Cfield([201, 201, 301, 201, 301, 301],  'i4', default=True)] #coupled to i3
            , 'test') 
        self.assertEqual(cdts.to_analysis()['relations'], dic['relations'])
        self.assertEqual(cdts.to_analysis()['name'], dic['name'])
        self.assertEqual(cdts.to_analysis()['length'], dic['length'])

class Test_AnaField_AnaRelation(unittest.TestCase):
    
    def test_creation(self):

        self.assertEqual(i0.to_dict(idfield=True), 
                         {'lencodec': 6, 'mincodec': 6, 'maxcodec': 6, 'id': 'i0'})
        self.assertEqual(i0.to_dict(full=True), 
                         {'lencodec': 6, 'mincodec': 6, 'maxcodec': 6, 'id': 'i0',
                          'dmincodec': 0, 'dmaxcodec': 0, 'rancodec': 0, 
                          'typecodec': 'complete'})        
        self.assertEqual(i2i1.to_dict(relation=True, mode='id'), 
                         {'dist': 3, 'parentchild': False, 'relation': ['i2', 'i1'], 'typecoupl': 'derived'})
        self.assertEqual(i2i1.to_dict(relation=True, distances=True, mode='id'), 
                         {'dist': 3, 'relation': ['i2', 'i1'], 'typecoupl': 'derived', 'parentchild': False,
                          'distance': 1, 'distomin': 0, 'distomax': 3, 'ratecpl': 0.25, 'rateder': 0.0})
        self.assertEqual(i2i1.to_dict(full=True, mode='id'), 
                         {'dist': 3, 'relation': ['i2', 'i1'], 'typecoupl': 'derived', 'parentchild': False,
                          'distance': 1, 'distomin': 0, 'distomax': 3, 'ratecpl': 0.25, 'rateder': 0.0,
                          'dmax': 6, 'dmin': 3, 'diff': 1, 'dran': 3})
        #print(dts.relations[fld1][fld2], dts.relations[fld2][fld1])
        self.assertTrue(dts.relations[AnaDfield(i1, dts)][AnaDfield(i2, dts)].dist == 
                        dts.relations[AnaDfield(i2, dts)][AnaDfield(i1, dts)].dist == 3)
        self.assertTrue(dts.relations[AnaDfield(i1, dts)][AnaDfield(i3, dts)].dist == 
                        dts.relations[AnaDfield(i3, dts)][AnaDfield(i1, dts)].dist == 6)
        self.assertEqual(dts, AnaDataset(dic))
        
    def test_casting(self):
        self.assertTrue(dts.dfield(dts.fields[0]) ==
                        dts.dfield(AnaField(dts.fields[0])) ==
                        dts.dfield('i0'))
        
    def test_field_typology(self):
        self.assertEqual([fld.category for fld in dts.fields], 
                         [ROOTED, MIXED, DERIVED, DERIVED, COUPLED])
        self.assertEqual([fld.p_derived.idfield for fld in dts.fields], 
                         [ROOT, ROOT, 'i1', ROOT, 'i3'])
        self.assertEqual([fld.typecodec for fld in dts.fields], 
                         [COMPLETE, DEFAULT, DEFAULT, DEFAULT, DEFAULT])
        self.assertEqual([fld.p_distance for fld in dts.fields], 
                         [dts.root, dts.root, dts.fields[1], dts.fields[2], dts.fields[3]])
        self.assertEqual([fld.list_parents() for fld in dts.fields], 
                         [[], [], [dts.fields[1]], [], [dts.fields[3]]])
        self.assertEqual([fld.list_parents('distance') for fld in dts.fields], 
                         [[], [], [dts.fields[1]], [dts.fields[2], dts.fields[1]],
                          [dts.fields[3], dts.fields[2], dts.fields[1]]])

    def test_tree(self):
        self.assertEqual(dts.tree(string=False), {'-1': ['root-derived (6)',
          {'0 ': ['i0 (0 - 6)']},
          {'1 ': ['i1 (3 - 3)', {'2 ': ['i2 (1 - 2)']}]},
          {'3 ': ['i3 (4 - 2)', {'4 ': ['i4 (0 - 2)']}]}]})
        self.assertEqual(dts.tree('distance', string=False), {'-1': ['root-distance (6)',
          {'0 ': ['i0 (0 - 6)']},
          {'1 ': ['i1 (3 - 3)',
            {'2 ': ['i2 (1 - 2)', {'3 ': ['i3 (2 - 2)', {'4 ': ['i4 (0 - 2)']}]}]}]}]})

    def test_partitions(self):
        self.assertEqual(dts.partitions('index', distributed=False), [[1, 3], [0]])
        self.assertEqual(dts.partitions('id', distributed=False), [['i1', 'i3'], ['i0']])
        
class Test_AnaDataset(unittest.TestCase):

    def test_sdataset(self):
        fruits = {'plants': ['fruit', 'fruit', 'fruit', 'fruit',
                                 'vegetable', 'vegetable', 'vegetable', 'vegetable'],
                     'plts': ['fr', 'fr', 'fr', 'fr', 've', 've', 've', 've'], 
                     'quantity': ['1 kg', '10 kg', '1 kg', '10 kg',
                                   '1 kg', '10 kg', '1 kg', '10 kg'],
                     'product': ['apple', 'apple', 'orange', 'orange',
                                  'peppers', 'peppers', 'carrot', 'carrot'],
                     'price': [1, 10, 2, 20, 1.5, 15, 1.5, 20],
                     'price level': ['low', 'low', 'high', 'high', 'low', 'low', 'high', 'high'],
                     'group': ['fruit 1', 'fruit 10', 'fruit 1', 'veget',
                                'veget', 'veget', 'veget', 'veget'],
                     'id': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
                     'supplier': ["sup1", "sup1", "sup1", "sup2", "sup2", "sup2", "sup2", "sup1"],
                     'location': 	["fr", "gb", "es", "ch", "gb", "fr", "es", "ch"],
                     'valid': ["ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok"]}
        ilm = Sdataset.ntv(fruits) 
        self.assertEqual(ilm.analysis.partitions('index'), [[0, 2, 5], [2, 5, 8], [0, 9], [2, 3], [8, 9], [7]])  
        
        ana = AnaDataset(ilm.to_analysis())
        self.assertEqual(ana.partitions('index', distributed=False), 
                         [[0, 2, 5], [0, 2, 8], [0, 5, 8], [2, 5, 8], [0, 9], [2, 3], [8, 9], [7]])
        ana = AnaDataset(ilm.to_analysis(True))
        self.assertEqual(ana.partitions('index'), [[0, 2, 5], [2, 5, 8], [0, 9], [2, 3], [8, 9], [7]])
        self.assertEqual(ana.field_partition(mode='index', distributed=False), 
                         {'primary': [0, 2, 5], 'secondary': [1], 'unique': [10], 'variable': [3, 4, 6, 7, 8, 9]})
        self.assertEqual(ana.field_partition(mode='index'), 
                         {'primary': [0, 2, 5], 'secondary': [1], 'unique': [10], 'variable': [3, 4, 6, 7, 8, 9]})
        self.assertEqual(ana.field_partition(mode='index', partition=ana.partitions()[1]), 
                         {'primary': [2, 5, 8], 'secondary': [], 'unique': [10], 'variable': [0, 1, 3, 4, 6, 7, 9]})
        self.assertEqual(ana.field_partition()['variable'], ana.variable)
        self.assertEqual(ana.field_partition()['primary'], ana.primary)
        self.assertEqual(ana.field_partition()['secondary'], ana.secondary)
        self.assertEqual(ana.field_partition()['unique'], ana.unique)

    def test_partitions(self):
        ilm = Sdataset.ntv({'i0': [1, 2, 3], 'test': [0, 1, 1]})
        self.assertEqual(ilm.partitions, [[0]])
        ilm = Sdataset.from_ntv({'i0': ['a', 'b', 'c'], 'i1': [1, 2, 2], 
                                 'i2': [4, 5, 5], 'i3': [6, 7, 8], 'i4': [6, 7, 8]})
        self.assertEqual(ilm.analysis.field_partition('index'), 
                         {'primary': [0], 'secondary': [1, 2, 3, 4], 'unique': [], 'variable': []})
        ilm = Sdataset.ntv([['math', 'english', 'software', 'physic', 'english', 'software'],
                         ['philippe', 'philippe', 'philippe',
                          'anne', 'anne', 'anne'],
                         [None, None, None, 'gr1', 'gr1', 'gr2'],
                         ['philippe white', 'philippe white', 'philippe white',
                          'anne white', 'anne white', 'anne white']])
        self.assertEqual(AnaDataset(ilm.to_analysis(True)).partitions('index'), [])
        ilm = Cdataset.from_ntv([['math', 'english', 'software', 'math', 'english', 'software'],
                          ['philippe', 'philippe', 'philippe', 'anne', 'anne', 'anne'],
                          [None, None, None, 'gr1', 'gr1', 'gr2'],
                          ['philippe white', 'philippe white', 'philippe white',
                           'anne white', 'anne white', 'anne white']])
        ana = AnaDataset(ilm.to_analysis(True))
        self.assertEqual(ana.partitions('index')[0], [0, 1])
        self.assertEqual(ana.dimension, 2)
        
        ilm = Cdataset.from_ntv([['er', 'rt', 'er', 'ry'], [0, 2, 0, 2], [30, 12, 12, 15],
                     [2, 0, 2, 0], [2, 2, 0, 0], ['info', 'info', 'info', 'info'], [12, 12, 15, 30]])
        ana = AnaDataset(ilm.to_analysis(True))
        self.assertEqual(ana.partitions('index')[0], [1, 4])
        
        ilm = Cdataset.from_ntv([['er', 'rt', 'er', 'ry'], [0, 2, 0, 2], [30, 12, 20, 30],
                     [2, 0, 2, 0], [2, 2, 0, 0], ['info', 'info', 'info', 'info'], [12, 20, 20, 12]])
        ana = AnaDataset(ilm.to_analysis(True))
        self.assertEqual(ana.partitions('index')[0], [1, 4])
        
        ilm = Cdataset.from_ntv([[0, 2, 0, 2], [30, 12, 12, 15], [2, 0, 2, 0], [2, 2, 0, 0],
                          ['info', 'info', 'info', 'info'], [12, 12, 15, 30]])
        ana = AnaDataset(ilm.to_analysis(True))
        self.assertEqual(ana.partitions('index')[0], [0, 3])
        
        ilm = Cdataset.from_ntv([[0, 2, 0, 2], [30, 12, 20, 30], [2, 0, 2, 0], [2, 2, 0, 0],
                          ['info', 'info', 'info', 'info'], [12, 20, 20, 12]])
        ana = AnaDataset(ilm.to_analysis(True))
        self.assertEqual(ana.partitions('index')[0], [0, 3])        

    def test_tree(self):
        il = Sdataset.ntv([[1,2,3,4], [5,6,7,8], [0,0,1,1]])
        self.assertEqual(AnaDataset(il.to_analysis(True)).tree(),
                         '-1: root-derived (4)\n   0 : i0 (0 - 4)\n   1 : i1 (0 - 4)\n   2 : i2 (2 - 2)')
        
if __name__ == '__main__':
    
    unittest.main(verbosity=2)
