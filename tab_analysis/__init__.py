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
from tab_analysis.analysis import AnaField, AnaRelation, AnaDataset, AnaDfield, Util
from tab_analysis.analysis import ROOT, ROOTED, DERIVED, COUPLED
from tab_analysis.analysis import NULL, UNIQUE, COMPLETE, FULL, DEFAULT, MIXED

# print('package :', __package__)
