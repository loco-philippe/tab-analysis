# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 23:06:12 2023

@author: philippe@loco-labs.io
"""
import unittest
from pprint import pprint
from tab_analysis import AnaField, AnaRelation, AnaDataset, AnaDfield

"""
il = Dataset.ntv([[1, 2, 3, 4, 5, 6], 
                  ['a', 'b', 'b', 'c', 'c', 'a'],
                  [20, 10, 10, 10, 10, 20], 
                  [200, 200, 300, 200, 300, 300]])
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

i0i0 = AnaRelation([i0, i0], 6)
i0i1 = AnaRelation([i0, i1], 6)
i0i2 = AnaRelation([i0, i2], 6)
i0i3 = AnaRelation([i0, i3], 6)

i1i0 = AnaRelation([i1, i0], 6)
i1i1 = AnaRelation([i1, i1], 3)
i1i2 = AnaRelation([i1, i2], 3)
i1i3 = AnaRelation([i1, i3], 6)

i2i0 = AnaRelation([i2, i0], 6)
i2i1 = AnaRelation([i2, i1], 3)
i2i2 = AnaRelation([i2, i2], 2)
i2i3 = AnaRelation([i2, i3], 4)

i3i0 = AnaRelation([i3, i0], 6)
i3i1 = AnaRelation([i3, i1], 6)
i3i2 = AnaRelation([i3, i2], 4)
i3i3 = AnaRelation([i3, i3], 2)

dts = AnaDataset([i0, i1, i2, i3])   
dts.set_relations(i0, {i1: 6, i2: 6, i3: 6})
dts.set_relations(i1, {i0: 6, i2: 3, i3: 6})
dts.set_relations(i2, {i0: 6, i1: 3, i3: 4})
dts.set_relations(i3, {i0: 6, i1: 6, i2: 4})

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
        self.assertEqual(i2i1.to_dict(relation=True, distance=True), 
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
        
if __name__ == '__main__':
    
    unittest.main(verbosity=2)
