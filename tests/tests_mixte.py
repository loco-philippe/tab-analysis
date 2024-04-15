# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:59:39 2024

@author: a lab in the Air
"""
import xarray as xr
import numpy as np
import ntv_pandas as npd
from analysis import Util

ds = xr.Dataset(
    {"foo": (("x", "y", "year"), np.random.randn(2, 3, 2))},
    coords={
        "x": [10, 20],
        "y": ["a", "b", "c"],
        "year": [2020, 2021],
        "point": (("x", "y"), np.array(["pt1", "pt2", "pt3", "pt4", "pt5", "pt6"]).reshape(2,3)),
        "along_x": ("x", np.random.randn(2)),
        "scalar": 123,
    })
df = ds.to_dataframe().reset_index()
ana = df.npd.analysis(distr=True)
print(Util.reduce_dic(ana.field_partition(mode='id')))
print(ana.partitions(mode='id'))

ds = xr.Dataset(
    {"foo": (("x", "y", "year"), np.random.randn(2, 3, 2))},
    coords={
        "x": [10, 20],
        "y": ["a", "a", "c"],
        "year": [2020, 2021],
        "point": (("x", "y"), np.array(["pt1", "pt2", "pt3", "pt4", "pt5", "pt6"]).reshape(2,3)),
        "along_x": ("x", np.random.randn(2)),
        "scalar": 123,
    })
df = ds.to_dataframe().reset_index()
ana = df.npd.analysis(distr=True)
print(Util.reduce_dic(ana.field_partition(mode='id'), notempty=True))
print(ana.partitions(mode='id'))