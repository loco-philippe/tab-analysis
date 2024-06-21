# -*- coding: utf-8 -*-
"""
This module analyses structure and relationships included in a tabular object
(Pandas DataFrame, Dataset, list of list) :
- Structure of a single field (class `AnaField`),
- Relationship between two fields (class `AnaRelation`)
- Structure and relationships of fields inside a dataset (class `AnaDfield`)
- Structure of a dataset (class `AnaDataset`)

It contains two another classes `Util`, `AnaError`.
"""

import json
import pprint
from itertools import combinations
from operator import mul
from functools import reduce

from time import time


NULL = "null"
UNIQUE = "unique"
COMPLETE = "complete"
FULL = "full"
DEFAULT = "default"
MIXED = "mixed"

COUPLED = "coupled"
DERIVED = "derived"
LINKED = "linked"
CROSSED = "crossed"
DISTRIBUTED = "distributed"
ROOTED = "rooted"
ROOT = "root"

IDFIELD = "id"
MINCODEC = "mincodec"
MAXCODEC = "maxcodec"
LENCODEC = "lencodec"
RATECODEC = "ratecodec"
DMINCODEC = "dmincodec"
DMAXCODEC = "dmaxcodec"
RANCODEC = "rancodec"
TYPECODEC = "typecodec"
HASHF = "hashf"
RELATION = "relation"
HASHR = "hashr"
DIST = "dist"
DMAX = "dmax"
DMIN = "dmin"
DIFF = "diff"
DRAN = "dran"
NUM = "num"
CATEGORY = "category"
PDERIVED = "pderived"
PDISTANCE = "pdistance"
PDISTOMIN = "pdistomin"
DISDISTANCE = "disdistance"
DERDISTANCE = "derdistance"
DISRATECPL = "disratecpl"
DERRATECPL = "derratecpl"
DISRATEDER = "disrateder"
DERRATEDER = "derrateder"

TYPECOUPL = "typecoupl"
PARENTCHILD = "parentchild"
DISTANCE = "distance"
DISTOMIN = "distomin"
DISTOMAX = "distomax"
DISTROOT = "distroot"
RATECPL = "ratecpl"
RATEDER = "rateder"

IDDATASET = "name"
RELATIONS = "relations"
FIELDS = "fields"
LENGTH = "length"
HASHD = "hashd"


class AnaField:
    """This class analyses field entities.

    *Attributes*

    - **idfield** : string - name or Id of the field
    - **lencodec**: integer - codec length
    - **mincodec**: integer - minimal codec length
    - **maxcodec**: integer - minimal codec length
    - **hashf**: integer - hash value to identify modifications

    *characteristic (@property)*

    - `iscomplete`
    - `ratecodec`
    - `dmincodec`
    - `dmaxcodec`
    - `rancodec`
    - `typecodec`

    *instance methods*

    - `to_dict`

    """

    def __init__(
        self, idfield, lencodec=None, mincodec=None, maxcodec=None, hashf=None
    ):
        """Creation mode :
        - single dict attribute where keys are attributes name,
        - single AnaField attribute to make a copy
        - multiple attributes

        *Parameters (multiple attributes)*

        - **idfield** : string or integer - Id of the Field
        - **lencodec** : integer (default None) - length of the codec
        - **mincodec** : integer (default None) - number of different values
        - **maxcodec** : integer (default None) - length of the field
        - **hashf** : string (default None) - update identifier

        *example*

        AnaField is created with a dict
        >>> AnaField(Cfield([1,2,3,3]).to_analysis).to_dict()
        {'lencodec': 4, 'mincodec': 3, 'maxcodec': 4}
        >>> AnaField({'lencodec': 4, 'mincodec': 3, 'maxcodec': 4})
        {'lencodec': 4, 'mincodec': 3, 'maxcodec': 4}

        AnaField is created with parameters
        >>> AnaField(lencodec=4, mincodec=3, maxcodec=4).to_dict()
        {'lencodec': 4, 'mincodec': 3, 'maxcodec': 4}
        >>> AnaField(4, 3, 4).to_dict()
        {'lencodec': 4, 'mincodec': 3, 'maxcodec': 4}
        """
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
        """length of the field (maxcodec)"""
        return self.maxcodec if self.maxcodec else self.lencodec

    def __repr__(self):
        """representation of the field (class name + idfield)"""
        return self.__class__.__name__ + "(" + str(self.idfield) + ")"

    def __eq__(self, other):
        """equal if class and attributes are equal"""
        return (
            self.__class__.__name__ == other.__class__.__name__
            and self.idfield == other.idfield
            and self.lencodec == other.lencodec
            and self.mincodec == other.mincodec
            and self.maxcodec == other.maxcodec
            and self.hashf == other.hashf
        )

    def __lt__(self, other):
        """return a comparison between hash value"""
        return hash(self) < hash(other)

    def __hash__(self):
        """return hash value (sum of attributes hash)"""
        return (
            hash(self.idfield)
            + hash(self.lencodec)
            + hash(self.mincodec)
            + hash(self.maxcodec)
            + hash(self.hashf)
        )

    def __str__(self):
        """json-text build with the attributes dict"""
        return json.dumps(self.to_dict(idfield=True))

    def __copy__(self):
        """Copy all the attributes"""
        return self.__class__(self)

    def to_dict(self, full=False, idfield=False, notnone=True):
        """return a dict with field attributes.

         *Parameters*

        - **full** : boolean (default False) - if True, all the attributes are included
        - **idfield** : boolean (default False) - if True, idfield is included
        - **notnone** : boolean (default True) - if True, None values are not included
        """
        dic = {
            LENCODEC: self.lencodec,
            MINCODEC: self.mincodec,
            MAXCODEC: self.maxcodec,
        }
        if idfield or full:
            dic[IDFIELD] = self.idfield
        if full:
            dic |= {
                RATECODEC: self.ratecodec,
                DMINCODEC: self.dmincodec,
                DMAXCODEC: self.dmaxcodec,
                RANCODEC: self.rancodec,
                TYPECODEC: self.typecodec,
            }
        if notnone:
            return Util.reduce_dic(dic)
        return dic

    @property
    def iscomplete(self):
        """return boolean indicator : True if all attributes are present"""
        return self.maxcodec is not None and self.mincodec is not None

    @property
    def ratecodec(self):
        """return float ratecodec indicator"""
        if self.iscomplete and self.maxcodec - self.mincodec:
            return (self.maxcodec - self.lencodec) / (self.maxcodec - self.mincodec)
        return None

    @property
    def dmincodec(self):
        """return integer dmincodec indicator"""
        return self.lencodec - self.mincodec if self.iscomplete else None

    @property
    def dmaxcodec(self):
        """return integer dmaxcodec indicator"""
        return self.maxcodec - self.lencodec if self.iscomplete else None

    @property
    def rancodec(self):
        """return integer rancodec indicator"""
        return self.maxcodec - self.mincodec if self.iscomplete else None

    @property
    def typecodec(self):
        """return string typecodec indicator
        (null, unique, complete, full, default, mixed)
        """
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
    """This class analyses relationship between two fields

    *Attributes* :

    - **relation** : List of the two fields involved in the relationship
    - **dist** : value of the relationship
    - **distrib** : boolean True if values are distributed
    - **hashr**: integer - hash value to identify update

    *global (@property)*

    - `id_relation`
    - `index_relation`
    - `parent_child`
    - `typecoupl`

    *characteristic (@property)*

    - `dmax`
    - `dmin`
    - `diff`
    - `dran`
    - `distomin`
    - `distomax`
    - `distance`
    - `ratecpl`
    - `rateder`

    *instance methods*

    - `to_dict`
    """

    def __init__(self, relation, dists, hashr=None):
        """Constructor of the relationship :

         *Parameters*

        - **relation** : List of the two fields involved in the relationship
        - **dists** : dist value or list of dist value and distrib boolean
        - **hashr**: integer - hash value to identify update
        """
        self.relation = relation
        if isinstance(dists, list):
            self.dist = dists[0]
            self.distrib = dists[1]
        else:
            self.dist = dists
            self.distrib = None
        self.hashr = hashr

    def __repr__(self):
        """representation of the field (class name + idfield)"""
        return self.__class__.__name__ + "(" + str(self.id_relation) + ")"

    def __str__(self):
        """json-text build with the attributes dict"""
        return json.dumps(self.to_dict(relation=True))

    def __eq__(self, other):
        """equal if class and values are equal"""
        return (
            self.__class__.__name__ == other.__class__.__name__
            and self.relation == other.relation
            and self.dist == other.dist
            and self.hashr == other.hashr
            and self.distrib == other.distrib
        )

    def __hash__(self):
        """return hash value (sum of attributes hash)"""
        return (
            hash(self.relation[0])
            + hash(self.relation[1])
            + hash(self.dist)
            + hash(self.hashr)
            + hash(self.distrib)
        )

    def to_dict(
        self,
        distances=False,
        full=False,
        mode="field",
        relation=False,
        notnone=True,
        misc=False,
    ):
        """return a dict with AnaRelation attributes.

         *Parameters*

        - **distances** : boolean (default False) - if True, distances indicators are included
        - **full** : boolean (default False) - if True, all the attributes are included
        - **relation** : boolean (default False) - if True, idfield are included
        - **notnone** : boolean (default True) - if True, None values are not included
        - **mode** : str (default 'field') - AnaDfield representation ('field', 'id', 'index')
        """
        dic = {DIST: self.dist, TYPECOUPL: self.typecoupl, HASHR: self.hashr}
        if relation or full:
            dic[RELATION] = Util.view(self.relation, mode)
            dic[PARENTCHILD] = self.parent_child
        if distances or full:
            dic |= {
                DISTANCE: self.distance,
                DISTOMIN: self.distomin,
                DISTOMAX: self.distomax,
                DISTRIBUTED: self.distrib,
                RATECPL: self.ratecpl,
                RATEDER: self.rateder,
            }
        if misc or full:
            dic |= {DMAX: self.dmax, DMIN: self.dmin, DIFF: self.diff, DRAN: self.dran}
        if notnone:
            return Util.reduce_dic(dic)
        return dic

    @property
    def id_relation(self):
        """return a list with the id of the two fields involved"""
        if self.relation:
            return [fld.idfield for fld in self.relation]
        return []

    @property
    def parent_child(self):
        """returns the direction of the relationship (True if parent is first)"""
        rel0 = self.relation[0]
        rel1 = self.relation[1]
        return rel0.lencodec > rel1.lencodec or (
            rel0.lencodec == rel1.lencodec and rel0.index < rel1.index
        )

    @property
    def index_relation(self):
        """return a list with the index of the two fields involved"""
        if self.relation:
            return [fld.index for fld in self.relation]
        return []

    @property
    def dmax(self):
        """return integer dmax indicator"""
        return self.relation[0].lencodec * self.relation[1].lencodec

    @property
    def dmin(self):
        """return integer dmin indicator"""
        return max(self.relation[0].lencodec, self.relation[1].lencodec)

    @property
    def diff(self):
        """return integer diff indicator"""
        return abs(self.relation[0].lencodec - self.relation[1].lencodec)

    @property
    def dran(self):
        """return integer dran indicator"""
        return self.dmax - self.dmin

    @property
    def distomin(self):
        """return integer distomin indicator"""
        return self.dist - self.dmin

    @property
    def distomax(self):
        """return integer distomax indicator"""
        return self.dmax - self.dist

    @property
    def distance(self):
        """return integer distance indicator"""
        return self.distomin + self.diff

    @property
    def ratecpl(self):
        """return float ratecpl indicator"""
        disdis = self.distance + self.distomax
        return 0 if disdis == 0 else self.distance / disdis

    @property
    def rateder(self):
        """return float rateder indicator"""
        return 0 if self.dran == 0 else self.distomin / self.dran

    @property
    def typecoupl(self):
        """return relationship type (coupled, derived, crossed, linked)"""
        if self.distance == 0:
            return COUPLED
        if self.distomin == 0:
            return DERIVED
        if self.distomax == 0:
            return CROSSED
        return LINKED


class AnaDfield(AnaField):
    """This class analyses structure and relationships of fields inside a dataset

    *Attributes* :

    - **dataset** : AnaDataset object where AnaDfield is included
    - **AnaField attributes** : inheritance of AnaField object

    *relationship (@property)*

    - `list_relations`
    - `list_p_derived`
    - `list_c_derived`
    - `list_coupled`

    *field (@property)*

    - `fields`
    - `p_derived`
    - `p_distance`
    - `p_distomin`

    *global (@property)*

    - `index`
    - `dist_root`
    - `category`

    *global (instance methods)*

    - `ascendants`
    - `to_dict`
    - `view`

    *other instance methods*

    - `dic_inner_node`
    """

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
        """AnaDfield is created by adding a AnaDataset link to an AnaField object.

         *Parameters*

        - **other** : AnaField or AnaDfield to initialize attributes
        - **dataset** : AnaDataset which includes the AnaDfield
        """
        self.dataset = dataset

    def __copy__(self):
        """Copy all the data"""
        return self.__class__(AnaField(self), self.dataset)

    def __lt__(self, other):
        """return a comparison between field index"""
        return self.index < other.index

    @property
    def index(self):
        """return the row of the field in the AnaDataset"""
        if self == self.dataset.root:
            return -1
        return self.dataset.fields.index(self)

    @property
    def fields(self):
        """return the list of the fields included in the AnaDataset"""
        return self.dataset.fields

    @property
    def list_relations(self):
        """return the list of the relations with the AnaDfield"""
        return list(self.dataset.relations[self].values())

    @property
    def list_p_derived(self):
        """return the list of the derived relations with the parents of AnaDfield"""
        return [
            rel
            for rel in self.list_relations
            if rel.typecoupl == DERIVED and not rel.parent_child
        ]

    @property
    def list_c_derived(self):
        """return the list of the derived relations with the childs of AnaDfield"""
        return [
            rel
            for rel in self.list_relations
            if rel.typecoupl == DERIVED
            and rel.parent_child
            and rel.relation[1].category != UNIQUE
        ]

    @property
    def list_coupled(self):
        """return the list of the coupled relations with the AnaDfield"""
        return [rel for rel in self.list_relations if rel.typecoupl == COUPLED]

    @property
    def dist_root(self):
        """return the distance to the root field"""
        return len(self.dataset) - self.lencodec

    @property
    def category(self):
        """return AnaDfield category (unique, rooted, coupled, derived, mixed)"""
        if self.typecodec == UNIQUE:
            return UNIQUE
        if self.typecodec in (COMPLETE, FULL):
            return ROOTED
        if COUPLED in [
            rel.typecoupl for rel in self.list_relations if not rel.parent_child
        ]:
            return COUPLED
        if not self.list_c_derived:
            return DERIVED
        return MIXED

    @property
    def p_derived(self):
        """return the first derived or coupled parent of the AnaDfield"""
        if self.category in (UNIQUE, ROOTED):
            return self.dataset.root
        if self.category == COUPLED:
            return [
                rel.relation[1]
                for rel in self.list_coupled
                if not rel.relation[1].category == COUPLED
            ][0]
        if not self.list_p_derived:
            return self.dataset.root
        distance_min = min(rel.distance for rel in self.list_p_derived)
        for rel in self.list_p_derived:
            if rel.distance == distance_min:
                if rel.relation[1].category == ROOTED:
                    return self.dataset.root
                if rel.relation[1].category == MIXED:
                    return rel.relation[1]
        return self.dataset.root

    @property
    def p_distance(self):
        """return the first parent with minimal distance of the AnaDfield"""
        return self._p_min_dist()

    @property
    def p_distomin(self):
        """return the first parent with minimal distomin of the AnaDfield"""
        return self._p_min_dist(False)

    def _p_min_dist(self, distance=True):
        """return the parent with minimal distance of the AnaDfield"""
        if self.category == UNIQUE:
            return self.dataset.root
        if distance:
            dist_up = [
                rel.distance for rel in self.list_relations if not rel.parent_child
            ]
        else:
            dist_up = [
                rel.distomin for rel in self.list_relations if not rel.parent_child
            ]
        if not dist_up or min(dist_up) == self.dist_root:
            return self.dataset.root
        dist_min = min(dist_up)
        if distance:
            list_dmin = [
                rel.relation[1]
                for rel in self.list_relations
                if rel.distance == dist_min
            ]
        else:
            list_dmin = [
                rel.relation[1]
                for rel in self.list_relations
                if rel.distomin == dist_min
            ]
        max_lencodec = max(fld.lencodec for fld in list_dmin)
        return [fld for fld in list_dmin if fld.lencodec == max_lencodec][0]

    def to_dict(self, mode="id"):
        """return a dict with field attributes.

         *Parameters*

        - **mode** : str (default 'id') - AnaDfield representation ('field', 'id', 'index')
        """
        dic = super().to_dict(full=True, idfield=False, notnone=False)
        dic[DISTROOT] = self.dist_root
        dic[NUM] = self.index
        dic[CATEGORY] = self.category
        dic[PDISTANCE] = self.p_distance.view(mode)
        dic[PDISTOMIN] = self.p_distomin.view(mode)
        dic[PDERIVED] = self.p_derived.view(mode)
        return dic

    def view(self, mode="field"):
        """return a representation of the AnaDfield

         *Parameters*

        - **mode** : str (default 'field') - AnaDfield representation ('field', 'id', 'index')
        """
        return Util.view(self, mode)

    def ascendants(self, typeparent="derived", mode="field"):
        """return the list of the AnaDfield's ascendants in the family tree up to
        the root AnaDfield.

         *Parameters*

        - **typeparent** : str (default 'derived') - 'derived', 'distance' or 'distomin'
        - **mode** : str (default 'field') - AnaDfield representation
        ('field', 'id', 'index')

        *Returns* : list of parents from closest to the most distant. Parents
        are represented with index, idfield, or object
        """
        parent = self
        listparent = []
        while parent != self.dataset.root:
            if typeparent == "derived":
                parent = parent.p_derived
            elif typeparent == "distance":
                parent = parent.p_distance
            else:
                parent = parent.p_distomin
            if parent != self.dataset.root:
                listparent.append(parent)
        return Util.view(listparent, mode)

    def dic_inner_node(self, mode, lname):
        """return a child AnaDfield tree.

         *Parameters*

        - **lname** : integer - maximal length of the names
        - **mode** : string (default 'derived') - kind of tree :
            'derived' : derived tree
            'distance': min distance tree
            'distomin': min distomin tree

        *Returns* : dict where key is a AnaDfield and value is the list of
        the childs "name ( dist - lencodec)".
        """
        adding = ""
        match mode:
            case "distance":
                rel_parent = self.dataset.get_relation(self, self.p_distance)
                adding = str(rel_parent.distance) + " - "
            case "distomin":
                rel_parent = self.dataset.get_relation(self, self.p_distomin)
                adding = str(rel_parent.distomin) + " - "
            case "derived":
                rel_parent = self.dataset.get_relation(self, self.p_derived)
                adding = str(rel_parent.distance) + " - "
            case _:
                ...
        adding += str(self.lencodec)
        name = str(self.idfield)[:lname] + " (" + adding + ")"
        lis = [name.replace(" ", "*").replace("'", "*")]
        match mode:
            case "derived":
                childs = []
                if self.category not in (ROOTED, COUPLED, UNIQUE):
                    for rel in self.list_coupled:
                        lis.append(rel.relation[1].dic_inner_node(mode, lname))
                if self.category not in (ROOTED, UNIQUE):
                    childs = [
                        rel.relation[1]
                        for rel in self.list_relations
                        if rel.relation[1].p_derived == self
                        and rel.relation[1].category != COUPLED
                    ]
            case "distomin":
                childs = [
                    rel.relation[1]
                    for rel in self.list_relations
                    if rel.relation[1].p_distomin == self
                ]
            case "distance":
                childs = [
                    rel.relation[1]
                    for rel in self.list_relations
                    if rel.relation[1].p_distance == self
                ]
        for fld in childs:
            lis.append(fld.dic_inner_node(mode, lname))
        return {str(self.index).ljust(2, "*"): lis}


class AnaDataset:
    """This class analyses the structure of a dataset.

    *Attributes* :

    - **iddataset** : string or integer - Id of the Dataset
    - **fields** : list of the AnaDfields included
    - **relations** : dict of the AnaRelations between two AnaDfields
    - **hashd** : string - update identifier

    *relationship (@property)*

    - `ana_relations`
    - `p_relations`

    *field (@property)*

    - `root`
    - `primary`
    - `secondary`
    - `unique`
    - `mixte`
    - `variable`

    *global (@property)*

    - `category`
    - `complete`
    - `dimension`

    *update (instance methods)*

    - `set_relations`

    *access (instance methods)*

    - `get_relation`
    - `dfield`

    *synthesis (instance methods)*

    - `tree`
    - `to_dict`
    - `indicator`
    - `partitions`
    - `field_partition`
    - `relation_partition`
    """

    def __init__(
        self, fields=None, relations=None, iddataset=None, leng=None, hashd=None
    ):
        """Creation mode :
        - single dict attribute where keys are attributes name,
        - single AnaDataset attribute to make a copy
        - multiple attributes

        *Parameters (single dict)*

        - **fields**: {'fields': list_of_dict, 'name': id_dataset,
                       'length': length, 'relations': dict_of_relations
            where:
                list_of_dict : {'id': id_field, 'lencodec': len_codec, 'mincodec': min_codec}
                id_field: string - name of field
                other_field: string - name of field
                len_codec: int - length of the codec
                min_codec: int - number of different codec values
                id_dataset : name of the dataset
                length: int - length of the dataset
                dict_of_relations: {id_field : {other_field: dist} for all fields}
                field: name of a field
                field_other: name of another field
                dist: integer (distance between the two fields) or
                array (distance and boolean distributed)

        *Parameters (multiple attributes)*

        - **fields**: list_of_dict
        - **iddataset** : string (default None) - id_dataset
        - **relations** : dict (default None) - dict_of_relations
        - **leng** : int (default None) - length
        - **hashd** : string (default None) - update identifier
        """
        if isinstance(fields, AnaDataset):
            self.iddataset = fields.iddataset
            self.fields = fields.fields
            self.relations = fields.relations
            self.hashd = fields.hashd
            #return
        else:
            if isinstance(fields, dict):
                iddataset = fields.get(IDDATASET, None)
                leng = fields.get(LENGTH, None)
                relations = fields.get(RELATIONS, None)
                hashd = fields.get(HASHD)
                fields = fields.get(FIELDS, None)
            self.iddataset = iddataset
            self.fields = (
                [AnaDfield(AnaField(field), self) for field in fields] if fields else []
            )
            if leng:
                for fld in self.fields:
                    fld.maxcodec = leng
            self.relations = {field: {} for field in self.fields}
            if relations:
                for fld, dic_relation in relations.items():
                    self.set_relations(fld, dic_relation)
            self.hashd = hashd
        
        self._len = max(len(fld) for fld in self.fields)
        self._root = AnaDfield(AnaField(ROOT, self._len, self._len, self._len), self)
        self._category = [fld.category for fld in self.fields]
        self._ana_relations = [rel for fldrel in self.relations.values() 
                               for rel in fldrel.values()]
        self._p_relations = [rel for rel in self.ana_relations if rel.parent_child]
        self._unique = [fld for fld in self.fields if fld.category == UNIQUE]
        self._partitions = self.set_partitions()
        self._primary = self.field_partition(mode="field")["primary"]
        self._secondary = self.field_partition(mode="field")["secondary"]
        self._variable = self.field_partition(mode="field")["variable"]
        self._mixte = self.field_partition(mode="field")["mixte"]
        
    def __len__(self):
        """length of the AnaDataset (len of the AnaDfields included)"""
        return self._len

    def __eq__(self, other):
        """equal if class and values are equal"""
        return (
            self.__class__.__name__ == other.__class__.__name__
            and self.fields == other.fields
            and self.relations == other.relations
            and self.iddataset == other.iddataset
            and self.hashd == other.hashd
        )

    def __hash__(self):
        """return hash value (sum of attributes hash)"""
        return (
            hash(self.iddataset)
            + sum(hash(fld) for fld in self.fields)
            + sum(hash(rel) for rel in self.relations)
            + hash(self.hashd)
        )

    @property
    def category(self):
        """return a list of AnaDfield category (unique, rooted, coupled, derived, mixed)"""
        return self._category

    @property
    def ana_relations(self):
        """return the list of AnaRelation included"""
        return self._ana_relations

    @property
    def p_relations(self):
        """return the list of oriented AnaRelation (parent first, child second)"""
        return self._p_relations

    @property
    def root(self):
        """return the root AnaDfield"""
        return self._root

    @property
    def primary(self):
        """return the first partition of the partitions"""
        return self._primary


    @property
    def complete(self):
        """return True if the dimension is not 0"""
        return self.dimension > 0

    @property
    def dimension(self):
        """return the highest partition lenght"""
        return len(self.primary)

    @property
    def secondary(self):
        """return the derived ou coupled fields from primary"""
        return self._secondary

    @property
    def unique(self):
        """return the unique fields"""
        return self._unique

    @property
    def variable(self):
        """return the variable fields"""
        return self._variable

    @property
    def mixte(self):
        """return the variable fields"""
        return self._mixte

    def set_relations(self, field, dic_relations):
        """Add relations in the AnaDataset from a dict.

         *Parameters*

        - **field** : AnaDfield, AnaField or str (idfield) - first relation AnaDfield
        - **dic_relations** : dict - key is the second relation AnaDfield and
        value is the dist value or teh list [dist, distrib]
        """
        fld = self.dfield(field)
        for other, dist in dic_relations.items():
            oth = self.dfield(other)
            self.relations[fld][oth] = AnaRelation([fld, oth], dist)
            self.relations[oth][fld] = AnaRelation([oth, fld], dist)

    def get_relation(self, fld1, fld2):
        """Return AnaRelation between fld1 and fld2.

         *Parameters*

        - **fld1** : AnaDfield, AnaField, int or str (idfield) - first relation AnaDfield
        - **fld2** : AnaDfield, AnaField, int or str (idfield) - second relation AnaDfield
        """
        fl1 = self.dfield(fld1)
        fl2 = self.dfield(fld2)
        if self.root in [fl1, fl2]:
            return AnaRelation([fl1, fl2], len(self))
        return self.relations[self.dfield(fld1)][self.dfield(fld2)]

    def dfield(self, fld):
        """return the AnaDfield matching with fld. Fld is str, int, AnaDfield or AnaField"""
        if fld in (-1, ROOT):
            return self.root
        if isinstance(fld, AnaDfield):
            return fld
        if isinstance(fld, int):
            return self.fields[fld]
        if isinstance(fld, str):
            if fld in [dfld.idfield for dfld in self.fields]:
                return [dfld for dfld in self.fields if dfld.idfield == fld][0]
            return None
        return AnaDfield(fld, self)

    def tree(self, mode="derived", width=5, lname=20, string=True):
        """return a string with a tree of derived Field.

         *Parameters*

        - **lname** : integer (default 20) - length of the names
        - **width** : integer (default 5) - length of the lines
        - **string** : boolean (default True) - if True return str else return dict
        - **mode** : string (default 'derived') - kind of tree :
            'derived' : derived tree
            'distance': min distance tree
            'distomin': min distomin tree
        """
        lis = ["root-" + mode + "*(" + str(len(self)) + ")"]
        if mode == "distance":
            childs = [fld for fld in self.fields if fld.p_distance == self.root]
        elif mode == "distomin":
            childs = [fld for fld in self.fields if fld.p_distomin == self.root]
        elif mode == "derived":
            childs = [fld for fld in self.fields if fld.p_derived == self.root]
        for fld in childs:
            lis.append(fld.dic_inner_node(mode, lname))
        tree = {str(-1).ljust(2, "*"): lis}
        if string:
            tre = pprint.pformat(tree, indent=0, width=width)
            tre = tre.replace("---", " - ")
            tre = tre.replace("  ", " ")
            tre = tre.replace("*", " ")
            for car in ["'", '"', "{", "[", "]", "}", ","]:
                tre = tre.replace(car, "")
            return tre
        return Util.clean_dic(tree, "*", " ")

    def to_dict(self, mode="field", keys=None, relations=False):
        """return a dict with fields attributes and optionaly relations attributes.

         *Parameters*

        - **mode** : str (default 'field') - AnaDfield representation
        ('field', 'id', 'index')
        - **relations** : boolean (default: False) - if False return a list of fields,
        if True return a dict '{"fields": <list of fields>, "relations": <list of relations>}'
        - **keys** : string, list or tuple - list of keys or single key to return
        if 'all' or None, all keys are returned
        if list, only keys in list are returned
        if string, only values associated to the string(key) are returned"""
        fields = Util.filter_dic([fld.to_dict(mode=mode) for fld in self.fields], keys)
        leng = len(self.fields)
        if not relations:
            return fields
        return {
            "fields": fields,
            "relations": [
                self.get_relation(i, j).to_dict(full=True, mode=mode)
                for i in range(-1, leng)
                for j in range(i + 1, leng)
            ],
        }

    def set_partitions(self):
        """return a list of available partitions (the first is highest)."""
        partit = [[fld] for fld in self.fields if fld.category == ROOTED]
        crossed = [
            rel
            for rel in self.ana_relations
            if rel.typecoupl == CROSSED
            and rel.parent_child
            and rel.relation[0].category != COUPLED
            and rel.relation[1].category != COUPLED
        ]
        crossed = [rel for rel in crossed if rel.distrib]
        if crossed and len(crossed) == 1 and crossed[0].dist == len(self):
            partit.insert(0, crossed[0].relation)
        elif crossed:
            for repeat in list(range(len(crossed))):
                candidates = combinations(crossed, repeat + 1)
                for candidat in candidates:
                    flds = list(
                        set(rel.relation[i] for rel in candidat for i in [0, 1])
                    )
                    if (
                        reduce(mul, [fld.lencodec for fld in flds]) == len(self)
                        and len(candidat) == sum(range(len(flds)))
                        and min(rel.distrib for rel in candidat)
                    ):
                        partit.insert(0, flds)
        return [
            list(tup)
            for tup in sorted(
                sorted(list({tuple(sorted(prt)) for prt in partit})),
                key=len,
                reverse=True,
            )
        ]
    
    def partitions(self, mode="id"):
        """return a list of available partitions (the first is highest).

         *Parameters*

        - **mode** : str (default 'id') - AnaDfield representation
        ('field', 'id', 'index')
        """
        return Util.view(self._partitions, mode)

    def field_partition(self, mode="id", partition=None):
        """return a partition dict with the list of primary, secondary, unique
        and variable fields.

        *Parameters*

        - **mode** : str (default 'id') - AnaDfield representation
        ('field', 'id', 'index')
        - **partition** : list of str, int, AnaDfield or AnaField(default None) -
        if None, partition used is the first calculated partition
        """
        t0 = time()

        partitions = self.partitions(mode="field")
        if not partitions:
            return Util.view(
                {
                    "primary": [],
                    "secondary": [fld for fld in self.fields if fld.category != UNIQUE],
                    "mixte": [],
                    "unique": [fld for fld in self.fields if fld.category == UNIQUE],
                    "variable": [],
                },
                mode,
            )
        if not partition:
            partition = partitions[0]
        else:
            partition = [self.dfield(fld) for fld in tuple(partition)]
        
        t1 = time()
        print('tf1 : ', t1-t0)
        
        secondary = []
        for field in partition:
            self._add_child(field, secondary)
        secondary = [fld for fld in secondary if fld not in partition]
        unique = [fld for fld in self.fields if fld.category == UNIQUE]
        
        t2 = time()
        print('tf2 : ', t2-t1)
        
        mixte = list(self._mixte_dims(partition, partitions))

        t3 = time()
        print('tf3 : ', t3-t2)
        
        variable = [
            fld
            for fld in self.fields
            if fld not in partition + secondary + unique + mixte
        ]
        return Util.view(
            {
                "primary": partition,
                "secondary": secondary,
                "mixte": mixte,
                "unique": unique,
                "variable": variable,
            },
            mode,
        )

    def relation_partition(self, partition=None, primary=False, noroot=False):
        """return a dict with the list of relationships for fields in a partition.

        *Parameters*

        - **partition** : list (default None) - if None, partition is the first
        - **primary** : boolean (default False) - if True, relations are primary fields
        - **noroot** : boolean (default False) - if True and single primary,
        'root' field is replaced by the primary field"""

        t0 = time()

        partitions = self.partitions(mode="field")
        if not partitions:
            partition = None
        else:
            partition = (
                Util.view(partition, mode="field", ana=self)
                if partition
                else partitions[0]
            )
        part = self.field_partition(mode="field", partition=partition)

        t1 = time()
        print('tr1 : ', t1-t0)
        
        fields_cat = {fld: cat for cat, l_fld in part.items() for fld in l_fld}
        
        t2 = time()
        print('tr2 : ', t2-t1)
        
        relations = {}
        for field in fields_cat:
            rel = []
            match fields_cat[field]:
                case "primary":
                    rel = [field.idfield]
                case "unique":
                    ...
                case "variable":
                    rel = [fld.idfield for fld in part["primary"]]
                case "secondary" if not primary:
                    rel = [field.p_derived.idfield]
                case "secondary" if primary:
                    rel = [
                        fld.idfield
                        for fld in field.ascendants()
                        if fld in part["primary"]
                    ]
                case "mixte":
                    rel = [
                        fld.idfield
                        for fld in self._mixte_dims(partition, partitions)[field]
                    ]
                case _:
                    ...
            if rel == ["root"] and len(part["primary"]) == 1 and noroot:
                rel = [part["primary"][0].idfield]
            if rel == ["root"] and len(part["primary"]) == 0 and noroot:
                rel = [part["secondary"][0].idfield]
            relations[field.idfield] = rel
        
        t3 = time()
        print('tr3 : ', t3-t2)
        
        return relations

    def indicator(self, fullsize, size):
        """generate size indicators: ol (object lightness), ul (unicity level),
        gain (sizegain)

        *Parameters*

        - **fullsize** : int - size with full codec
        - **size** : int - size with existing codec

        *Returns* : dict"""
        lenindex = len(self.fields)
        indexlen = sum(fld.lencodec for fld in self.fields)
        nval = len(self) * (lenindex + 1)
        sval = fullsize / nval
        ncod = indexlen + lenindex

        if nval != ncod:
            scod = (size - ncod * sval) / (nval - ncod)
            olight = scod / sval
        else:
            olight = None
        return {
            "total values": nval,
            "mean size": round(sval, 3),
            "unique values": ncod,
            "mean coding size": round(scod, 3),
            "unicity level": round(ncod / nval, 3),
            "optimize level": round(size / fullsize, 3),
            "object lightness": round(olight, 3),
            "maxgain": round((nval - ncod) / nval, 3),
            "gain": round((fullsize - size) / fullsize, 3),
        }

    def _add_child(self, field, childs):
        """add derived or coupled fields in the childs list"""
        for rel in field.list_c_derived + field.list_coupled:
            child = rel.relation[1]
            if child not in childs and not child.category == UNIQUE:
                childs.append(child)
                if child.category not in (COUPLED, UNIQUE):
                    self._add_child(child, childs)

    def _mixte_dims(self, partition, partitions):
        """return dict with dimensions associated to each mixte field"""
        dic_mixte = {}
        for part in partitions:
            not_part = [fld for fld in part if fld not in partition]
            if len(not_part) == 1 and len(partition) > len(part) > 1:
                sub_part = [fld for fld in partition if fld not in part]
                if (
                    min(
                        self.get_relation(not_part[0], fld).typecoupl == "derived"
                        for fld in sub_part
                    )
                    is True
                ):
                    dic_mixte[not_part[0]] = sub_part
        return dic_mixte


class Util:
    """common functions for analysis package"""

    @staticmethod
    def view(field_struc, mode, ana=None):
        """return a representation of a AnaDfields structure (field, id, index).

         *Parameters*

        - **mode** : str - AnaDfield representation ('field', 'id', 'index')
        - **field_struc** : list or dict - structure to represent
        - **ana** : AnaDataset (default None) - to convert string or index in AnaDfield
        """

        if mode is None or not field_struc:
            return field_struc
        if isinstance(field_struc, dict):
            return {
                key: Util.view(val, mode=mode, ana=ana)
                for key, val in field_struc.items()
            }
        if isinstance(field_struc, list):
            return [Util.view(val, mode=mode, ana=ana) for val in field_struc]
        if not isinstance(field_struc, AnaDfield) and mode != "id":
            return Util.view(ana.dfield(field_struc), mode=mode)
        return (
            field_struc
            if mode == "field"
            else (field_struc.index if mode == "index" else field_struc.idfield)
        )

    @staticmethod
    def reduce_dic(obj, notempty=False):
        """return a dict without None values"""
        if isinstance(obj, dict):
            return {
                key: Util.reduce_dic(val)
                for key, val in obj.items()
                if val is not None and (not notempty or val)
            }
        if isinstance(obj, list):
            return [Util.reduce_dic(val) for val in obj]
        return obj

    @staticmethod
    def clean_dic(obj, old, new):
        """return a dict or list with updated strings by replacing "old" substring
        with "new" substring"""
        if isinstance(obj, dict):
            return {
                Util.clean_dic(key, old, new): Util.clean_dic(val, old, new)
                for key, val in obj.items()
            }
        if isinstance(obj, str):
            return obj.replace(old, new)
        if isinstance(obj, list):
            return [Util.clean_dic(val, old, new) for val in obj]
        return obj

    @staticmethod
    def filter_dic(obj, keys):
        """return extract of a list of dict or of a dict

         *Parameters*

        - **keys** : string, list or tuple - list of keys or single key to return
        if 'all' or None, all keys are returned
        if list, only keys in list are returned
        if string, only values associated to the string(key) are returned"""
        if not keys or keys == "all":
            return obj
        if isinstance(obj, list):
            return [Util.filter_dic(dic, keys) for dic in obj]
        if isinstance(keys, str) and isinstance(obj, dict):
            return obj.get(keys, None)
        if isinstance(keys, (list, tuple)) and isinstance(obj, dict):
            return {key: val for key, val in obj.items() if key in keys}
        return obj


class AnaError(Exception):
    """Analysis Exception"""
