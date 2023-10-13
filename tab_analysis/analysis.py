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
RANCODEC = 'rancodec'
TYPECODEC = 'typecodec'
HASHF = 'hashf'

RELATION = 'relation'
HASHR = 'hashr'
DIST = 'dist'
DMAX = 'dmax'
DMIN = 'dmin'
DIFF = 'diff'
DRAN = 'dran'

TYPECOUPL = 'typecoupl'
DISTANCE = 'distance'
DISTOMIN = 'distomin'
DISTOMAX = 'distomax'
RATECPL  = 'ratecpl'
RATEDER  = 'rateder'

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
   
    def __init__(self, idfield, lencodec, mincodec=None, maxcodec=None, hashf=None):
        if not isinstance(lencodec, int):
            raise AnalysisError("lencodec is not correct")
        self.idfield = idfield
        self.lencodec = lencodec
        self.mincodec = mincodec
        self.maxcodec = maxcodec
        self.hashf = hashf
        #AnaField.id_field[idfield] = self

    def __repr__(self):
        rep = IDFIELD + ': ' + str(self.idfield) + '\n' + '    ' 
        return rep + json.dumps(self.to_dict())
    
    def __str__(self):
        return json.dumps(self.to_dict(idfield=True))

    def to_dict(self, full=False, idfield=False, notnone=True):
        dic = {LENCODEC: self.lencodec, MINCODEC: self.mincodec, 
               MAXCODEC: self.maxcodec, HASHF: self.hashf}
        if idfield or full:
            dic[IDFIELD] = self.idfield
        if full:
            dic |= {RATECODEC: self.ratecodec, DMINCODEC: self.dmincodec,
                    DMAXCODEC: self.dmaxcodec, RANCODEC: self.rancodec,
                    TYPECODEC: self.typecodec}
        if notnone:
            return Util.reduce_dic(dic)
        return dic

    @property
    def iscomplete(self):
        return not self.maxcodec is None and not self.mincodec is None
    
    @property
    def ratecodec(self):
        if self.iscomplete and self.maxcodec - self.mincodec:
            return (self.maxcodec - self.lencodec) / (self.maxcodec - self.mincodec)
        return None

    @property
    def dmincodec(self):
        return self.lencodec - self.mincodec if self.iscomplete else None
    
    @property
    def dmaxcodec(self):
        return self.maxcodec - self.lencodec if self.iscomplete else None
    
    @property
    def rancodec(self):
        return self.maxcodec - self.mincodec if self.iscomplete else None

    @property
    def typecodec(self):
        if self.maxcodec is None or self.mincodec is None:
            return None
        if self.maxcodec == 0:
            return 'null'
        if self.lencodec == 1:
            return 'unique'
        if self.mincodec == self.maxcodec:
            return 'complete'
        if self.lencodec == self.maxcodec:
            return 'full'
        if self.lencodec == self.mincodec:
            return 'default'
        return 'mixed'        
    
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
        self.relation = relation
        #if isinstance(relation, (list, tuple)) and len(relation) == 2:
            #self.relation = relation 
            #self.relation = [rel if isinstance(rel, AnaField) else 
            #    AnaField.id_field[rel] for rel in relation]
        self.dist = dist
        self.hashr = hashr

    def __repr__(self):
        rep = RELATION + ': ' + str(self.id_relation) + '\n' + '    ' 
        return rep + json.dumps(self.to_dict())
    
    def __str__(self):
        return json.dumps(self.to_dict(relation=True))

    def to_dict(self, distance=False, full=False, relation=False, notnone=True):
        dic = {DIST: self.dist, HASHR: self.hashr}
        if relation or full:
            dic[RELATION] = self.id_relation
            dic[TYPECOUPL] = self.typecoupl
        if distance or full:
            dic |= {DISTANCE: self.distance, DISTOMIN: self.distomin,
                    DISTOMAX: self.distomax, RATECPL: self.ratecpl,
                    RATEDER: self.rateder}
        if full:
            dic |= {DMAX: self.dmax, DMIN: self.dmin,
                    DIFF: self.diff, DRAN: self.dran}
        if notnone:
            return Util.reduce_dic(dic)
        return dic
    
    @property
    def id_relation(self):
        if self.relation:
            return [rel.idfield for rel in self.relation]
        return []

    @property 
    def dmax(self):
        return self.relation[0].lencodec * self.relation[1].lencodec

    @property 
    def dmin(self):
        return max(self.relation[0].lencodec, self.relation[1].lencodec)

    @property 
    def diff(self):
        return abs(self.relation[0].lencodec - self.relation[1].lencodec)

    @property 
    def dran(self):
        return self.dmax - self.dmin

    @property 
    def distomin(self):
        return self.dist - self.dmin
    
    @property 
    def distomax(self):
        return self.dmax - self.dist

    @property 
    def distance(self):
        return self.distomin + self.diff

    @property 
    def ratecpl(self):
        return self.distance / (self.distance + self.distomax)

    @property 
    def rateder(self):
        return self.distomin / self.dran

    @property
    def typecoupl(self):
        if self.distance == 0:
            return 'coupled'
        if self.distomin == 0:
            return 'derived'
        if self.distomax == 0:
            return 'crossed'
        return 'linked'
    
class AnaDataset:

    def __init__(self, fields=None, relations=None, hashd=None):
        self.fields = fields
        self.relations = {field: {} for field in fields}
        if relations:
            self.relations |= relations
        self.hashd = hashd

    def set_relations(self, field, dic_relations):
        for other, dist in dic_relations.items():
            self.relations[field][other] = AnaRelation([field, other], dist)
            self.relations[other][field] = AnaRelation([other, field], dist)
            
class Util:

    @staticmethod 
    def reduce_dic(dic):
        return {key: val for key, val in dic.items() if not val is None}    

class AnalysisError(Exception):
    ''' Analysis Exception'''
    # pass