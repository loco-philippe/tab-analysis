# -*- coding: utf-8 -*-
"""
***TAB-analysis Package***

Created on Oct 2023

@author: philippe@loco-labs.io

This package contains the following classes and functions:

- `tab-analysis.tab_analysis.analysis` :

    - `tab-analysis.tab_analysis.analysis.AnaField`
    - `tab-analysis.tab_analysis.analysis.AnaRelation`
    - `tab-analysis.tab_analysis.analysis.AnaDfield`
    - `tab-analysis.tab_analysis.analysis.AnaDataset`
    - `tab-analysis.tab_analysis.analysis.Util`
    - `tab-analysis.tab_analysis.analysis.AnaError`
    
    
"""
from tab_analysis.analysis import AnaField, AnaRelation, AnaDataset, AnaDfield
from tab_analysis.analysis import ROOT, ROOTED, ROOTDERIVED, DERIVED, COUPLED
from tab_analysis.analysis import NULL, UNIQUE, COMPLETE, FULL, DEFAULT, MIXED

#print('package :', __package__)