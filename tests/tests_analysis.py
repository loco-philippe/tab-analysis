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
il.lindex[0].infos
{'lencodec': 6, 'mincodec': 6, 'maxcodec': 6, 'typecodec': 'complete', 'ratecodec': 0.0}
il.lindex[1].infos
{'lencodec': 3, 'mincodec': 3, 'maxcodec': 6, 'typecodec': 'default', 'ratecodec': 1.0}
il.lindex[2].infos
{'lencodec': 2, 'mincodec': 2, 'maxcodec': 6, 'typecodec': 'default', 'ratecodec': 1.0}
il.lindex[3].infos
{'lencodec': 2, 'mincodec': 2, 'maxcodec': 6, 'typecodec': 'default', 'ratecodec': 1.0}
il.couplingmatrix()[0]
[{'dist': 6,  'distmin': 6,  'distmax': 36,  'diff': 0,  'rateder': 0.0,  'disttomin': 0,  
  'disttomax': 30,  'distance': 0,  'ratecpl': 0.0,  'typecoupl': 'coupled'},
 {'dist': 6,  'distmin': 6,  'distmax': 18,  'diff': 3,  'rateder': 0.0,  'disttomin': 0,
  'disttomax': 12,  'distance': 3,  'ratecpl': 0.2,  'typecoupl': 'derive'},
 {'dist': 6,  'distmin': 6,  'distmax': 12,  'diff': 4,  'rateder': 0.0,  'disttomin': 0,
  'disttomax': 6,  'distance': 4,  'ratecpl': 0.4,  'typecoupl': 'derive'},
 {'dist': 6,  'distmin': 6,  'distmax': 12,  'diff': 4,  'rateder': 0.0,  'disttomin': 0,
  'disttomax': 6,  'distance': 4,  'ratecpl': 0.4,  'typecoupl': 'derive'}]
il.couplingmatrix()[1]
[{'dist': 6,  'distmin': 6,  'distmax': 18,  'diff': 3,  'rateder': 0.0,  'disttomin': 0,  
  'disttomax': 12,  'distance': 3,  'ratecpl': 0.2,  'typecoupl': 'derived'},
 {'dist': 3,  'distmin': 3,  'distmax': 9,  'diff': 0,  'rateder': 0.0,  'disttomin': 0,
  'disttomax': 6,  'distance': 0,  'ratecpl': 0.0,  'typecoupl': 'coupled'},
 {'dist': 3,  'distmin': 3,  'distmax': 6,  'diff': 1,  'rateder': 0.0,  'disttomin': 0,
  'disttomax': 3,  'distance': 1,  'ratecpl': 0.25,  'typecoupl': 'derive'},
 {'dist': 6,  'distmin': 3,  'distmax': 6,  'diff': 1,  'rateder': 1.0,  'disttomin': 3,
  'disttomax': 0,  'distance': 4,  'ratecpl': 1.0,  'typecoupl': 'crossed'}]
il.couplingmatrix()[2]
[{'dist': 6,  'distmin': 6,  'distmax': 12,  'diff': 4,  'rateder': 0.0,  'disttomin': 0,  
  'disttomax': 6,  'distance': 4,  'ratecpl': 0.4,  'typecoupl': 'derived'},
 {'dist': 3,  'distmin': 3,  'distmax': 6,  'diff': 1,  'rateder': 0.0,  'disttomin': 0,
  'disttomax': 3,  'distance': 1,  'ratecpl': 0.25,  'typecoupl': 'derived'},
 {'dist': 2,  'distmin': 2,  'distmax': 4,  'diff': 0,  'rateder': 0.0,  'disttomin': 0,
  'disttomax': 2,  'distance': 0,  'ratecpl': 0.0,  'typecoupl': 'coupled'},
 {'dist': 4,  'distmin': 2,  'distmax': 4,  'diff': 0,  'rateder': 1.0,  'disttomin': 2,
  'disttomax': 0,  'distance': 2,  'ratecpl': 1.0,  'typecoupl': 'crossed'}]
il.couplingmatrix()[3]
[{'dist': 6,  'distmin': 6,  'distmax': 12,  'diff': 4,  'rateder': 0.0,  'disttomin': 0,  
  'disttomax': 6,  'distance': 4,  'ratecpl': 0.4,  'typecoupl': 'derived'},
 {'dist': 6,  'distmin': 3,  'distmax': 6,  'diff': 1,  'rateder': 1.0,  'disttomin': 3,
  'disttomax': 0,  'distance': 4,  'ratecpl': 1.0,  'typecoupl': 'crossed'},
 {'dist': 4,  'distmin': 2,  'distmax': 4,  'diff': 0,  'rateder': 1.0,  'disttomin': 2,
  'disttomax': 0,  'distance': 2,  'ratecpl': 1.0,  'typecoupl': 'crossed'},
 {'dist': 2,  'distmin': 2,  'distmax': 4,  'diff': 0,  'rateder': 0.0,  'disttomin': 0,
  'disttomax': 2,  'distance': 0,  'ratecpl': 0.0,  'typecoupl': 'coupled'}]
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
        self.assertEqual(cdts.analys()['relations'], dic['relations'])
        self.assertEqual(cdts.analys()['name'], dic['name'])
        self.assertEqual(cdts.analys()['length'], dic['length'])

class Test_AnaField_AnaRelation(unittest.TestCase):
    
    def test_creation(self):

        self.assertEqual(i0.to_dict(idfield=True), 
                         {'lencodec': 6, 'mincodec': 6, 'maxcodec': 6, 'id': 'i0'})
        self.assertEqual(i0.to_dict(full=True), 
                         {'lencodec': 6, 'mincodec': 6, 'maxcodec': 6, 'id': 'i0',
                          'dmincodec': 0, 'dmaxcodec': 0, 'rancodec': 0, 
                          'typecodec': 'complete'})        
        self.assertEqual(i2i1.to_dict(relation=True), 
                         {'dist': 3, 'relation': ['i2', 'i1'], 'typecoupl': 'derived'})
        self.assertEqual(i2i1.to_dict(relation=True, distances=True), 
                         {'dist': 3, 'relation': ['i2', 'i1'], 'typecoupl': 'derived',
                          'distance': 1, 'distomin': 0, 'distomax': 3, 'ratecpl': 0.25, 'rateder': 0.0})
        self.assertEqual(i2i1.to_dict(full=True), 
                         {'dist': 3, 'relation': ['i2', 'i1'], 'typecoupl': 'derived',
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
                         #[ROOTED, ROOTDERIVED, DERIVED, ROOTDERIVED, COUPLED])
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

    def test_partition(self):
        self.assertEqual(dts.partition('index', distributed=False), [[1, 3], [0]])
        self.assertEqual(dts.partition('id', distributed=False), [['i1', 'i3'], ['i0']])
        
class Test_AnaDataset(unittest.TestCase):

    def test_sdataset(self):
        fruits = {'plants': ['fruit', 'fruit', 'fruit', 'fruit',
                                 'vegetable', 'vegetable', 'vegetable', 'vegetable'],
                     'quantity': ['1 kg', '10 kg', '1 kg', '10 kg',
                                   '1 kg', '10 kg', '1 kg', '10 kg'],
                     'product': ['apple', 'apple', 'orange', 'orange',
                                  'peppers', 'peppers', 'banana', 'banana'],
                     'price': [1, 10, 2, 20, 1.5, 15, 1, 1.5],
                     'group': ['fruit 1', 'fruit 10', 'fruit 1', 'veget',
                                'veget', 'veget', 'veget', 'veget'],
                     'id': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
                     'supplier': ["sup1", "sup1", "sup1", "sup2", "sup2", "sup2", "sup2", "sup1"],
                     'location': 	["fr", "gb", "es", "ch", "gb", "fr", "es", "ch"]}
        ilm = Sdataset.ntv(fruits) 
        self.assertEqual(ilm.analysis.getpartition(), [[0, 7], [1, 2], [6, 7], [5]])
        
        ilm = Cdataset.from_ntv(fruits)
        ana = AnaDataset(ilm.analys(True))
        self.assertEqual(ana.partition('index'), [[0, 7], [1, 2], [6, 7], [5]])
        ana = AnaDataset(ilm.analys())
        self.assertEqual(ana.partition('index', distributed=False), [[0, 1, 6], [0, 7], [1, 2], [6, 7], [5]])

    def test_primary(self):
        ilm = Cdataset.from_ntv([['math', 'english', 'software', 'math', 'english', 'software'],
                          ['philippe', 'philippe', 'philippe', 'anne', 'anne', 'anne'],
                          [None, None, None, 'gr1', 'gr1', 'gr2'],
                          ['philippe white', 'philippe white', 'philippe white',
                           'anne white', 'anne white', 'anne white']])
        ana = AnaDataset(ilm.analys(True))
        self.assertEqual(ana.partition('index')[0], [0, 1])
        self.assertEqual(ana.dimension, 2)
        
        ilm = Cdataset.from_ntv([['er', 'rt', 'er', 'ry'], [0, 2, 0, 2], [30, 12, 12, 15],
                     [2, 0, 2, 0], [2, 2, 0, 0], ['info', 'info', 'info', 'info'], [12, 12, 15, 30]])
        ana = AnaDataset(ilm.analys(True))
        self.assertEqual(ana.partition('index')[0], [1, 4])
        
        ilm = Cdataset.from_ntv([['er', 'rt', 'er', 'ry'], [0, 2, 0, 2], [30, 12, 20, 30],
                     [2, 0, 2, 0], [2, 2, 0, 0], ['info', 'info', 'info', 'info'], [12, 20, 20, 12]])
        ana = AnaDataset(ilm.analys(True))
        self.assertEqual(ana.partition('index')[0], [1, 4])
        
        ilm = Cdataset.from_ntv([[0, 2, 0, 2], [30, 12, 12, 15], [2, 0, 2, 0], [2, 2, 0, 0],
                          ['info', 'info', 'info', 'info'], [12, 12, 15, 30]])
        ana = AnaDataset(ilm.analys(True))
        self.assertEqual(ana.partition('index')[0], [0, 3])
        
        ilm = Cdataset.from_ntv([[0, 2, 0, 2], [30, 12, 20, 30], [2, 0, 2, 0], [2, 2, 0, 0],
                          ['info', 'info', 'info', 'info'], [12, 20, 20, 12]])
        ana = AnaDataset(ilm.analys(True))
        self.assertEqual(ana.partition('index')[0], [0, 3])        
        
if __name__ == '__main__':
    
    unittest.main(verbosity=2)
