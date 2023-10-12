# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:49:34 2023

@author: philippe@loco-labs.io
"""
import json

IDFIELD = 'id'
MINCODEC = 'mincodec'
MAXCODEC = 'maxcodec'
LENCODEC = 'lencodec'
RATECODEC = 'ratecodec'
DMINCODEC = 'dmincodec'
DMAXCODEC = 'dmaxcodec'
RANGECODEC = 'rangecodec'
HASHF = 'hashf'

RELATION = 'relation'
HASHR = 'hashr'
DIST = 'dist'


class AnaField:
    '''This class analyses relationships included in a tabular object 
    (Pandas DataFrame, Dataset, Observation, list of list).

    The Analysis class includes the following functions:
    - identification and qualification of the relationships between Field,
    - generation of the global properties of the structure
    - data actualization based on structure updates

    *Attributes* :

    - **iobj** : Dataset or Observation associated to the Analysis object
    '''    
    id_field = {}

    @classmethod 
    @property
    def field_id(cls):
        return {val:key for key, val in cls.id_field.items()}
    
    def __init__(self, idfield, lencodec, mincodec=None, maxcodec=None, hashf=None):
        self.idfield = idfield
        self.lencodec = lencodec
        self.mincodec = mincodec
        self.maxcodec = maxcodec
        self.hashf = hashf
        AnaField.id_field[idfield] = self

    def __repr__(self):
        rep = IDFIELD + ': ' + str(self.idfield) + '\n' + '    ' 
        return rep + json.dumps({LENCODEC: self.lencodec, MINCODEC: self.mincodec,
                                 MAXCODEC: self.maxcodec})
    
    def __str__(self):
        return json.dumps({IDFIELD: self.idfield, LENCODEC: self.lencodec, MINCODEC: self.mincodec,
                           MAXCODEC: self.maxcodec})
    @property
    def ratecodec(self):
        if (self.maxcodec and self.mincodec and self.lencodec and 
            self.maxcodec - self.mincodec):
            return (self.maxcodec - self.lencodec) / (self.maxcodec - self.mincodec)
        return None

    @property
    def dmincodec(self):
        if self.mincodec and self.lencodec:
            return self.lencodec - self.mincodec
        return None
    
    @property
    def dmaxcodec(self):
        if self.maxcodec and self.lencodec:
            return self.maxcodec - self.lencodec
        return None
    
    @property
    def rangecodec(self):
        if self.maxcodec and self.mincodec:
            return self.maxcodec - self.mincodec
        return None
    
class AnaRelation:
        '''This class analyses relationships included in a tabular object 
        (Pandas DataFrame, Dataset, Observation, list of list).

        The Analysis class includes the following functions:
        - identification and qualification of the relationships between Field,
        - generation of the global properties of the structure
        - data actualization based on structure updates

        *Attributes* :

        - **iobj** : Dataset or Observation associated to the Analysis object
        '''    
        
        def __init__(self, relation, dist, hashr=None):
            self.relation = []
            if isinstance(relation, (list, tuple)) and len(relation) == 2:
                self.relation = [rel if isinstance(rel, AnaField) else 
                    AnaField.id_field[rel] for rel in relation]
            self.dist = dist
            self.hashr = hashr

        def __repr__(self):
            rep = RELATION + ': ' + str(self.id_relation) + '\n' + '    ' 
            return rep + json.dumps({DIST: self.dist, HASHR: self.hashr})
        
        def __str__(self):
            return json.dumps({RELATION: self.id_relation, DIST: self.dist, 
                               HASHR: self.hashr})
        @property
        def id_relation(self):
            if self.relation:
                return [AnaField.field_id[self.relation[0]],
                        AnaField.field_id[self.relation[1]]]
            return []
        