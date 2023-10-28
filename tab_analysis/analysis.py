# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:49:34 2023

@author: philippe@loco-labs.io

This module analyses structure and relationships included in a tabular object
(Pandas DataFrame, Dataset, list of list) :
- Structure of a single field (class `AnaField`),
- Relationship between two fields (class `AnaRelation`)
- Structure and relationships of fields inside a dataset (class `AnaDfield`)
- Structure of a dataset (class `AnaDataset`)

It contains the classes `AnaField`, `AnaRelation`,
`AnaDfield`, `AnaDataset`, `Util`, `AnaError`.

"""
import json
import pprint
from itertools import combinations
from operator import mul
from functools import reduce

NULL = 'null'
UNIQUE = 'unique'
COMPLETE = 'complete'
FULL = 'full'
DEFAULT = 'default'
MIXED = 'mixed'

COUPLED = 'coupled'
DERIVED = 'derived'
LINKED = 'linked'
CROSSED = 'crossed'
DISTRIBUTED = 'distributed'
ROOTED = 'rooted'
ROOTDERIVED = 'root derived'
ROOT = 'root'

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
RATECPL = 'ratecpl'
RATEDER = 'rateder'

IDDATASET = 'name'
RELATIONS = 'relations'
FIELDS = 'fields'
LENGTH = 'length'


class AnaField:
    '''This class analyses field entities.

    *Attributes*

    - **idfield** : string - name or Id of the field
    - **lencodec**: integer - codec length
    - **mincodec**: integer - minimal codec length
    - **maxcodec**: integer - minimal codec length
    - **hashf**: integer - hash value to identify modifications

    *dynamic values (@property)*

    - `iscomplete`
    - `ratecodec`
    - `dmincodec`
    - `dmaxcodec`
    - `rancodec`
    - `typecodec`

    *instance methods*

    - `to_dict`

    '''

    def __init__(self, idfield, lencodec=None, mincodec=None, maxcodec=None, hashf=None):
        '''Creation mode :
        - single dict attribute where keys are attributes name,
        - single AnaField attribute to make a copy
        - multiple attributes

        *Parameters (multiple attributes)*

        - **idfield** : string or integer - Id of the Field
        - **lencodec** : integer (default None) - length of the codec
        - **mincodec** : integer (default None) - number of different values
        - **maxcodec** : integer (default None) - length of the field
        - **hashf** : string (default None) - update identifier
        '''
        if isinstance(idfield, dict):
            self.idfield = idfield.get(IDFIELD, None)
            self.lencodec = idfield.get(LENCODEC, None)
            self.mincodec = idfield.get(MINCODEC, None)
            self.maxcodec = idfield.get(MAXCODEC, None)
            self.hashf = idfield.get(HASHF, None)
            return
        if isinstance(idfield, (AnaField, AnaDfield)):
            self.idfield = idfield.idfield
            self.lencodec = idfield.lencodec
            self.mincodec = idfield.mincodec
            self.maxcodec = idfield.maxcodec
            self.hashf = idfield.hashf
            return
        if not lencodec or not isinstance(lencodec, int):
            raise AnaError("lencodec is not correct")
        self.idfield = idfield
        self.lencodec = lencodec
        self.mincodec = mincodec
        self.maxcodec = maxcodec
        self.hashf = hashf

    def __len__(self):
        '''length of the field (maxcodec)'''
        return self.maxcodec if self.maxcodec else self.lencodec

    def __repr__(self):
        '''representation of the field (class name + idfield)'''
        return self.__class__.__name__ + '(' + self.idfield + ')'

    def __eq__(self, other):
        ''' equal if class and attributes are equal'''
        return self.__class__ .__name__ == other.__class__.__name__ and \
            self.idfield == other.idfield and self.lencodec == other.lencodec and \
            self.mincodec == other.mincodec and self.maxcodec == other.maxcodec and \
            self.hashf == other.hashf

    def __lt__(self, other):
        ''' return a comparison between hash value'''
        return hash(self) < hash(other)

    def __hash__(self):
        '''return hash value (sum of attributes hash)'''
        return hash(self.idfield) + hash(self.lencodec) + hash(self.mincodec) \
            + hash(self.maxcodec) + hash(self.hashf)

    def __str__(self):
        '''json-text build with the attributes dict'''
        return json.dumps(self.to_dict(idfield=True))

    def __copy__(self):
        ''' Copy all the attributes '''
        return self.__class__(self)

    def to_dict(self, full=False, idfield=False, notnone=True):
        '''return a dict with field attributes.

         *Parameters*

        - **full** : boolean (default False) - if True, all the attributes are included
        - **idfield** : boolean (default False) - if True, idfield is included
        - **notnone** : boolean (default True) - if True, None values are not included
        '''
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
        '''return boolean indicator : True if all attributes are present'''
        return not self.maxcodec is None and not self.mincodec is None

    @property
    def ratecodec(self):
        '''return float ratecodec indicator'''
        if self.iscomplete and self.maxcodec - self.mincodec:
            return (self.maxcodec - self.lencodec) / (self.maxcodec - self.mincodec)
        return None

    @property
    def dmincodec(self):
        '''return integer dmincodec indicator'''
        return self.lencodec - self.mincodec if self.iscomplete else None

    @property
    def dmaxcodec(self):
        '''return integer dmaxcodec indicator'''
        return self.maxcodec - self.lencodec if self.iscomplete else None

    @property
    def rancodec(self):
        '''return integer rancodec indicator'''
        return self.maxcodec - self.mincodec if self.iscomplete else None

    @property
    def typecodec(self):
        '''return string typecodec indicator
        (null, unique, complete, full, default, mixed)
        '''
        if self.maxcodec is None or self.mincodec is None:
            return None
        if self.maxcodec == 0:
            return NULL
        if self.lencodec == 1:
            return UNIQUE
        if self.mincodec == self.maxcodec:
            return COMPLETE
        if self.lencodec == self.maxcodec:
            return FULL
        if self.lencodec == self.mincodec:
            return DEFAULT
        return MIXED


class AnaRelation:
    '''This class analyses relationship between two fields

    *Attributes* :

    - **relation** : List of the two fields involved in the relationship
    - **dist** : value of the relationship
    - **distrib** : boolean True if values are distributed
    - **hashr**: integer - hash value to identify update

    *dynamic values (@property)*

    - `id_relation`
    - `index_relation`
    - `dmax`
    - `dmin`
    - `diff`
    - `dran`
    - `distomin`
    - `distomax`
    - `distance`
    - `ratecpl`
    - `rateder`
    - `typecoupl`

    *instance methods*

    - `to_dict`
    '''

    def __init__(self, relation, dists, hashr=None):
        '''Constructor of the relationship :

         *Parameters*

        - **relation** : List of the two fields involved in the relationship
        - **dists** : dist value or list of dist value and distrib boolean
        - **distrib** : boolean True if values are distributed
        - **hashr**: integer - hash value to identify update
        '''
        self.relation = relation
        if isinstance(dists, list):
            self.dist = dists[0]
            self.distrib = dists[1]
        else:
            self.dist = dists
            self.distrib = None
        self.hashr = hashr

    def __repr__(self):
        '''representation of the field (class name + idfield)'''
        return self.__class__.__name__ + '(' + str(self.id_relation) + ')'

    def __str__(self):
        '''json-text build with the attributes dict'''
        return json.dumps(self.to_dict(relation=True))

    def __eq__(self, other):
        ''' equal if class and values are equal'''
        return self.__class__ .__name__ == other.__class__.__name__ and \
            self.relation == other.relation and self.dist == other.dist and \
            self.hashr == other.hashr and self.distrib == other.distrib

    def __hash__(self):
        '''return hash value (sum of attributes hash)'''
        return hash(self.relation[0]) + hash(self.relation[1]) + \
            hash(self.dist) + hash(self.hashr) + hash(self.distrib)

    def to_dict(self, distances=False, full=False, relation=False, notnone=True):
        '''return a dict with AnaRelation attributes.

         *Parameters*

        - **distances** : boolean (default False) - if True, distances indicators are included
        - **full** : boolean (default False) - if True, all the attributes are included
        - **relation** : boolean (default False) - if True, idfield are included
        - **notnone** : boolean (default True) - if True, None values are not included
        '''
        dic = {DIST: self.dist, HASHR: self.hashr}
        if relation or full:
            dic[RELATION] = self.id_relation
            dic[TYPECOUPL] = self.typecoupl
        if distances or full:
            dic |= {DISTANCE: self.distance, DISTOMIN: self.distomin,
                    DISTOMAX: self.distomax, DISTRIBUTED: self.distrib,
                    RATECPL: self.ratecpl, RATEDER: self.rateder}
        if full:
            dic |= {DMAX: self.dmax, DMIN: self.dmin,
                    DIFF: self.diff, DRAN: self.dran}
        if notnone:
            return Util.reduce_dic(dic)
        return dic

    @property
    def id_relation(self):
        '''return a list with the id of the two fields involved'''
        if self.relation:
            return [fld.idfield for fld in self.relation]
        return []

    @property
    def index_relation(self):
        '''return a list with the index of the two fields involved'''
        if self.relation:
            return [fld.index for fld in self.relation]
        return []

    @property
    def dmax(self):
        '''return integer dmax indicator'''
        return self.relation[0].lencodec * self.relation[1].lencodec

    @property
    def dmin(self):
        '''return integer dmin indicator'''
        return max(self.relation[0].lencodec, self.relation[1].lencodec)

    @property
    def diff(self):
        '''return integer diff indicator'''
        return abs(self.relation[0].lencodec - self.relation[1].lencodec)

    @property
    def dran(self):
        '''return integer dran indicator'''
        return self.dmax - self.dmin

    @property
    def distomin(self):
        '''return integer distomin indicator'''
        return self.dist - self.dmin

    @property
    def distomax(self):
        '''return integer distomax indicator'''
        return self.dmax - self.dist

    @property
    def distance(self):
        '''return integer distance indicator'''
        return self.distomin + self.diff

    @property
    def ratecpl(self):
        '''return float ratecpl indicator'''
        return self.distance / (self.distance + self.distomax)

    @property
    def rateder(self):
        '''return float rateder indicator'''
        return self.distomin / self.dran

    @property
    def typecoupl(self):
        '''return relationship type (coupled, derived, crossed, linked)'''
        if self.distance == 0:
            return COUPLED
        if self.distomin == 0:
            return DERIVED
        if self.distomax == 0:
            return CROSSED
        return LINKED


class AnaDfield(AnaField):
    '''This class analyses structure and relationships of fields inside a dataset

    *Attributes* :

    - **dataset** : AnaDataset object where AnaDfield is included
    - **AnaField attributes** : inheritance of AnaField object

    *dynamic values (@property)*

    - `index`
    - `fields`
    - `list_relations`
    - `list_p_derived`
    - `list_c_derived`
    - `list_coupled`
    - `dist_root`
    - `category`
    - `p_derived`
    - `p_distance`

    *instance methods*

    - `list_parents`
    - `dic_inner_node`
    '''
    def __new__(cls, other, dataset=None):
        '''initialization of attributes from "other"'''
        if isinstance(other, AnaDfield):
            new = AnaDfield.__copy__(other)
            return new
        if isinstance(other, AnaField):
            new = AnaField.__copy__(other)
            new.__class__ = AnaDfield
            return new
        return object.__new__(cls)

    def __init__(self, other, dataset):
        '''AnaDfield is created by adding a AnaDataset link to an AnaField object.

         *Parameters*

        - **other** : AnaField or AnaDfield to initialize attributes
        - **dataset** : AnaDataset which includes the AnaDfield
        '''
        self.dataset = dataset

    def __copy__(self):
        ''' Copy all the data '''
        return self.__class__(AnaField(self), self.dataset)

    def __lt__(self, other):
        ''' return a comparison between field index'''
        return self.index < other.index

    @property
    def index(self):
        '''return the row of the field in the AnaDataset'''
        if self == self.dataset.root:
            return -1
        return self.dataset.fields.index(self)

    @property
    def fields(self):
        '''return the list of the fields included in the AnaDataset'''
        return self.dataset.fields

    @property
    def list_relations(self):
        '''return the list of the relations with the AnaDfield'''
        return list(self.dataset.relations[self].values())

    @property
    def list_p_derived(self):
        '''return the list of the derived relations with the parents of AnaDfield'''
        return [rel for rel in self.list_relations if rel.typecoupl == DERIVED
                and rel.relation[1].lencodec > self.lencodec]

    @property
    def list_c_derived(self):
        '''return the list of the derived relations with the childs of AnaDfield'''
        return [rel for rel in self.list_relations if rel.typecoupl == DERIVED
                and rel.relation[1].lencodec < self.lencodec]

    @property
    def list_coupled(self):
        '''return the list of the coupled relations with the AnaDfield'''
        return [rel for rel in self.list_relations if rel.typecoupl == COUPLED]

    @property
    def dist_root(self):
        '''return the distance to the root field'''
        return len(self.dataset) - self.lencodec

    @property
    def category(self):
        '''return AnaDfield category (unique, rooted, coupled, derived, mixed)'''
        if self.typecodec == UNIQUE:
            return UNIQUE
        if self.typecodec in (COMPLETE, FULL):
            return ROOTED
        if COUPLED in [rel.typecoupl for rel in self.list_relations
                       if rel.relation[1].index < self.index]:
            return COUPLED
        if not self.list_c_derived:
            return DERIVED
        return MIXED

    @property
    def p_derived(self):
        '''return the derived parent of the AnaDfield'''
        if self.category in (UNIQUE, ROOTED, ROOTDERIVED):
            return self.dataset.root
        if self.category == COUPLED:
            return [rel.relation[1] for rel in self.list_coupled
                    if not rel.relation[1].category == COUPLED][0]
        distance_min = min(rel.distance for rel in self.list_p_derived)
        for rel in self.list_p_derived:
            if rel.distance == distance_min:
                if rel.relation[1].category == ROOTED:
                    return self.dataset.root
                if rel.relation[1].category in (MIXED, ROOTDERIVED):
                    return rel.relation[1]
        return self.dataset.root

    @property
    def p_distance(self):
        '''return the parent with minimal distance of the AnaDfield'''
        if self.category in (UNIQUE, ROOTED, COUPLED):
            return self.p_derived
        dist_up = [rel.distance for rel in self.list_relations
                   if rel.relation[1].lencodec >= self.lencodec
                   and rel.relation[1].category != COUPLED]
        if not dist_up or min(dist_up) == self.dist_root:
            return self.dataset.root
        distance_min = min(dist_up)
        list_dmin = [rel.relation[1] for rel in self.list_relations
                     if rel.distance == distance_min]
        max_lencodec = max(fld.lencodec for fld in list_dmin)
        return [fld for fld in list_dmin if fld.lencodec == max_lencodec][0]

    def list_parents(self, typeparent='derived', mode='field'):
        ''' return the list of the AnaDfield's parents in the family tree up to
        the root AnaDfield.

         *Parameters*

        - **typeparent** : str (default 'derived') - 'derived' or 'distance'
        - **mode** : str (default 'field') - AnaDfield representation
        ('field', 'id', 'index')

        *Returns* : list of parents from closest to the most distant. Parents
        are represented with index, idfield, or object
        '''
        parent = self
        listparent = []
        while parent != self.dataset.root:
            parent = parent.p_derived if typeparent == 'derived' else parent.p_distance
            if parent != self.dataset.root:
                listparent.append(parent)
        return Util.view(listparent, mode)

    def dic_inner_node(self, mode, lname):
        '''return a child AnaDfield tree.

         *Parameters*

        - **lname** : integer - maximal length of the names
        - **mode** : str (default 'field') - AnaDfield representation
        ('field', 'id', 'index')

        *Returns* : dict where key is a AnaDfield and value is the list of
        the childs.
        '''
        adding = ''
        if mode == 'distance':
            rel_parent = self.dataset.get_relation(self, self.p_distance)
            adding = str(rel_parent.distance) + ' - '
        elif mode == 'derived':
            rel_parent = self.dataset.get_relation(self, self.p_derived)
            adding = str(rel_parent.distance) + ' - '
        adding += str(self.lencodec)
        name = self.idfield[:lname] + ' (' + adding + ')'
        lis = [name.replace(' ', '*').replace("'", '*')]
        if self.category != COUPLED:
            for rel in self.list_coupled:
                lis.append(rel.relation[1].dic_inner_node(mode, lname))
        if not self.category in (ROOTED, UNIQUE):
            if mode == 'distance':
                childs = [rel.relation[1] for rel in self.list_relations
                          if rel.relation[1].p_distance == self and
                          rel.relation[1].category != COUPLED]
            elif mode == 'derived':
                childs = [rel.relation[1] for rel in self.list_relations
                          if rel.relation[1].p_derived == self and
                          rel.relation[1].category != COUPLED]
            for fld in childs:
                lis.append(fld.dic_inner_node(mode, lname))
        return {str(self.index).ljust(2, '*'): lis}


class AnaDataset:
    '''This class analyses the structure of a dataset.

    *Attributes* :

    - **iddataset** : string or integer - Id of the Dataset
    - **fields** : list of the AnaDfields included
    - **relations** : dict of the AnaRelations between two AnaDfields
    - **hashd** : string - update identifier

    *dynamic values (@property)*

    - `ana_relations`
    - `root`
    - `primary`
    - `dimension`

    *instance methods*

    - `set_relations`
    - `get_relation`
    - `dfield`
    - `tree`
    - `partitions`
    - `field_partition`
    '''

    def __init__(self, fields=None, relations=None, iddataset=None,
                 leng=None, hashd=None):
        '''Creation mode :
        - single dict attribute where keys are attributes name,
        - single AnaDataset attribute to make a copy
        - multiple attributes

         *Parameters (multiple attributes)*

        - **idfield** : string or integer - Id of the Field
        - **lencodec** : integer (default None) - length of the codec
        - **mincodec** : integer (default None) - number of different values
        - **maxcodec** : integer (default None) - length of the field
        - **hashf** : string (default None) - update identifier
        '''
        if isinstance(fields, AnaDataset):
            self.iddataset = fields.iddataset
            self.fields = fields.fields
            self.relations = fields.relations
            self.hashd = fields.hashd
            return
        if isinstance(fields, dict):
            iddataset = fields.get(IDDATASET, None)
            leng = fields.get(LENGTH, None)
            relations = fields.get(RELATIONS, None)
            hashd = fields.get(hashd)
            fields = fields.get(FIELDS, None)
        self.iddataset = iddataset
        self.fields = [AnaDfield(AnaField(field), self)
                       for field in fields] if fields else []
        if leng:
            for fld in self.fields:
                fld.maxcodec = leng
        self.relations = {field: {} for field in self.fields}
        if relations:
            for fld, dic_relation in relations.items():
                self.set_relations(fld, dic_relation)
        self.hashd = hashd

    def __len__(self):
        '''length of the AnaDataset (len of the AnaDfields included)'''
        return max(len(fld) for fld in self.fields)

    def __eq__(self, other):
        ''' equal if class and values are equal'''
        return self.__class__ .__name__ == other.__class__.__name__ and \
            self.fields == other.fields and self.relations == other.relations and \
            self.iddataset == other.iddataset and self.hashd == other.hashd

    def __hash__(self):
        '''return hash value (sum of attributes hash)'''
        return hash(self.iddataset) + sum(hash(fld) for fld in self.fields) + \
            sum(hash(rel) for rel in self.relations) + hash(self.hashd)

    @property
    def ana_relations(self):
        '''return the list of AnaRelation included'''
        return [rel for fldrel in self.relations.values() for rel in fldrel.values()]

    @property
    def root(self):
        '''return the root AnaDfield'''
        len_self = len(self)
        return AnaDfield(AnaField(ROOT, len_self, len_self, len_self), self)

    @property
    def primary(self):
        '''return the first partition of the partitions'''
        part = self.partitions()
        return part[0] if part else []

    @property
    def dimension(self):
        '''return the highest partition lenght'''
        return len(self.primary)

    def set_relations(self, field, dic_relations):
        '''Add relations in the AnaDataset from a dict.

         *Parameters*

        - **field** : AnaDfield, AnaField or str (idfield) - first relation AnaDfield
        - **dic_relations** : dict - key is the second relation AnaDfield and
        value is the dist value or teh list [dist, distrib]
        '''
        fld = self.dfield(field)
        for other, dist in dic_relations.items():
            oth = self.dfield(other)
            self.relations[fld][oth] = AnaRelation([fld, oth], dist)
            self.relations[oth][fld] = AnaRelation([oth, fld], dist)

    def get_relation(self, fld1, fld2):
        '''Return AnaRelation between fld1 and fld2.

         *Parameters*

        - **fld1** : AnaDfield, AnaField or str (idfield) - first relation AnaDfield
        - **fld2** : AnaDfield, AnaField or str (idfield) - second relation AnaDfield
        '''
        fl1 = self.dfield(fld1)
        fl2 = self.dfield(fld2)
        if self.root in [fl1, fl2]:
            return AnaRelation([fl1, fl2], len(self))
        return self.relations[self.dfield(fld1)][self.dfield(fld2)]

    def dfield(self, fld):
        '''return the AnaDfield matching with fld. Fld is str, AnaDfield or AnaField'''
        if isinstance(fld, AnaDfield):
            return fld
        if isinstance(fld, str):
            if fld in [dfld.idfield for dfld in self.fields]:
                return [dfld for dfld in self.fields if dfld.idfield == fld][0]
            return self.root
        return AnaDfield(fld, self)

    def tree(self, mode='derived', width=5, lname=20, string=True):
        '''return a string with a tree of derived Field.

         *Parameters*

        - **lname** : integer (default 20) - length of the names
        - **width** : integer (default 5) - length of the lines
        - **string** : boolean (default True) - if True return str else return dict
        - **mode** : string (default 'derived') - kind of tree :
            'derived' : derived tree
            'distance': min distance tree
        '''
        lis = ['root-' + mode + '*(' + str(len(self)) + ')']
        if mode == 'distance':
            childs = [fld for fld in self.fields if fld.p_distance == self.root]
        elif mode == 'derived':
            childs = [fld for fld in self.fields if fld.p_derived == self.root]
        for fld in childs:
            lis.append(fld.dic_inner_node(mode, lname))
        tree = {str(-1).ljust(2, '*'): lis}
        if string:
            tre = pprint.pformat(tree, indent=0, width=width)
            tre = tre.replace('---', ' - ')
            tre = tre.replace('  ', ' ')
            tre = tre.replace('*', ' ')
            for car in ["'", "\"", "{", "[", "]", "}", ","]:
                tre = tre.replace(car, "")
            return tre
        return Util.clean_dic(tree, '*', ' ')

    def partitions(self, mode='field', distributed=True):
        '''return a list of available partitions (the first is highest).

         *Parameters*

        - **mode** : str (default 'field') - AnaDfield representation
        ('field', 'id', 'index')
        - **distributed** : boolean (default True) - Include only distributed fields
        '''
        crossed = [rel for rel in self.ana_relations if rel.typecoupl == CROSSED
                   and rel.relation[1].index > rel.relation[0].index
                   and rel.relation[0].category != COUPLED
                   and rel.relation[1].category != COUPLED]
        if distributed:
            crossed = [rel for rel in crossed if rel.distrib]
        if not crossed:
            return []
        partit = [[fld] for fld in self.fields if fld.category == ROOTED]
        if len(crossed) == 1 and crossed[0].dist == len(self):
            partit.insert(0, crossed[0].relation)
        else:
            for repeat in list(range(len(crossed))):
                candidates = combinations(crossed, repeat + 1)
                for candidat in candidates:
                    flds = list(set(rel.relation[i]
                                for rel in candidat for i in [0, 1]))
                    if (reduce(mul, [fld.lencodec for fld in flds]) == len(self) and
                        len(candidat) == sum(range(len(flds))) and
                            (not distributed or min(rel.distrib for rel in candidat))):
                        partit.insert(0, flds)
        partit = Util.view(partit, mode)
        return [list(tup) for tup in
                sorted(sorted(list({tuple(sorted(prt)) for prt in partit})),
                       key=len, reverse=True)]

    def field_partition(self, mode='field', partition=None, distributed=True):
        '''return a partition dict with the list of primary, secondary and variable fields.

         *Parameters*

        - **mode** : str (default 'field') - AnaDfield representation
        ('field', 'id', 'index')
        - **partition** : list (default None) - if None, partition is the first
        - **distributed** : boolean (default True) - Include only distributed fields
        '''
        if not partition:
            partitions = self.partitions(distributed=distributed)
            if not partitions:
                return {'primary': [], 'secondary': [], 'variable': []}
            partition = partitions[0]
        secondary = []
        for field in partition:
            self._add_child(field, secondary)
        variable = [
            fld for fld in self.fields if not fld in partition + secondary]
        return Util.view({'primary': partition, 'secondary': secondary,
                          'variable': variable}, mode)

    def _add_child(self, field, childs):
        ''' add derived or coupled fields in the childs list'''
        for rel in field.list_c_derived + field.list_coupled:
            childs.append(rel.relation[1])
            self._add_child(rel.relation[1], childs)


class Util:
    ''' common functions for analysis package'''

    @staticmethod
    def view(field_struc, mode):
        ''' return a representation of a AnaDfields structure (fields, id, index).

         *Parameters*

        - **mode** : str - AnaDfield representation ('field', 'id', 'index')
        - **field_struc** : list or dict - structure to represent
        '''
        if mode is None or mode == 'field' or not field_struc:
            return field_struc
        if isinstance(field_struc, dict):
            if mode == 'id':
                return {key: [fld.idfield for fld in val] for key, val in field_struc.items()}
            if mode == 'index':
                return {key: [fld.index for fld in val] for key, val in field_struc.items()}
        if isinstance(field_struc, list) and isinstance(field_struc[0], list):
            if mode == 'id':
                return [[fld.idfield for fld in val] for val in field_struc]
            if mode == 'index':
                return [[fld.index for fld in val] for val in field_struc]
        if isinstance(field_struc, list):
            if mode == 'id':
                return [fld.idfield for fld in field_struc]
            if mode == 'index':
                return [fld.index for fld in field_struc]
        return field_struc

    @staticmethod
    def reduce_dic(dic):
        '''return a dict without empty or None values'''
        return {key: val for key, val in dic.items() if not val is None}

    @staticmethod
    def clean_dic(obj, old, new):
        '''return a dict or list with updated strings by replacing "old" substring
        with "new" substring'''
        if isinstance(obj, dict):
            return {Util.clean_dic(key, old, new): Util.clean_dic(val, old, new)
                    for key, val in obj.items()}
        if isinstance(obj, str):
            return obj.replace(old, new)
        if isinstance(obj, list):
            return [Util.clean_dic(val, old, new) for val in obj]
        return obj


class AnaError(Exception):
    ''' Analysis Exception'''
    # pass
