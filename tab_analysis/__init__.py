# -*- coding: utf-8 -*-
"""
***TAB-analysis Package***

This package contains the following classes and functions:

- module `tab-analysis.tab_analysis.analysis` :

    - `tab-analysis.tab_analysis.analysis.AnaField`
    - `tab-analysis.tab_analysis.analysis.AnaRelation`
    - `tab-analysis.tab_analysis.analysis.AnaDfield`
    - `tab-analysis.tab_analysis.analysis.AnaDataset`
    - `tab-analysis.tab_analysis.analysis.Util`
    - `tab-analysis.tab_analysis.analysis.AnaError`

For more information, see the
[user guide](https://loco-philippe.github.io/tab-analysis/docs/user_guide.html)
or the [github repository](https://github.com/loco-philippe/tab-analysis).
"""

from tab_analysis.analysis import AnaField as AnaField
from tab_analysis.analysis import AnaRelation as AnaRelation
from tab_analysis.analysis import AnaDataset as AnaDataset
from tab_analysis.analysis import AnaDfield as AnaDfield
from tab_analysis.analysis import Util as Util
from tab_analysis.analysis import ROOT as ROOT
from tab_analysis.analysis import ROOTED as ROOTED
from tab_analysis.analysis import DERIVED as DERIVED
from tab_analysis.analysis import COUPLED as COUPLED
from tab_analysis.analysis import NULL as NULL
from tab_analysis.analysis import UNIQUE as UNIQUE
from tab_analysis.analysis import COMPLETE as COMPLETE
from tab_analysis.analysis import FULL as FULL
from tab_analysis.analysis import DEFAULT as DEFAULT
from tab_analysis.analysis import MIXED as MIXED
