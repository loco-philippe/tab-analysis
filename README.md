### *TAB-analysis : A tool to Analyse tabular and multi-dimensionnal structures*

*TAB-analysis analyzes and measures the relationships between Fields in any tabular Dataset.*

*The TAB-analysis tool is part of the [Environmental Sensing Project](https://github.com/loco-philippe/Environmental-Sensing#readme)*

For more information, see the [user guide](https://loco-philippe.github.io/tab-analysis/docs/user_guide.html) or the [github repository](https://github.com/loco-philippe/tab-analysis).

# What is TAB-analysis ?

## Principles

Each field in a dataset has global properties (e.g. the number of different values).
The relationships between two fields can also be characterized in a similar way (e.g. number of pairs of values from the two different fields).

Analyzing these properties gives us a measure of the entire dataset.

The TAB-analysis module carries out these measurements and analyzes. It also identifies data that does not respect given relationships.

## Examples

Here is a price list of different foods based on packaging.

| 'plants'    | 'quantity' | 'product' | 'price' |
|-------------|------------|-----------|---------|
| 'fruit'     | '1 kg'     | 'apple'   | 1       |
| 'fruit'     | '10 kg'    | 'apple'   | 10      |
| 'fruit'     | '1 kg'     | 'orange'  | 2       |
| 'fruit'     | '10 kg'    | 'orange'  | 20      |
| 'vegetable' | '1 kg'     | 'peppers' | 1.5     |
| 'vegetable' | '10 kg'    | 'peppers' | 15      |
| 'vegetable' | '1 kg'     | 'carrot'  | 0.5     |
| 'vegetable' | '10 kg'    | 'carrot'  | 5       |

In this example, we observe two kinds of relationships:

- classification ("derived" relationship): between 'plants' and 'product' (each product belongs a plant)
- crossing ("crossed" relationship): between 'product' and 'quantity' (all the combinations of the two fields are present).

This Dataset can be translated in a matrix between 'quantity' ['1 kg', '10 kg'] and 'product' ['apple', 'orange', 'peppers', 'carrot']

```python
In [1]: # creation of the `analysis` object 
        from tab_dataset import Sdataset
        from tab_analysis import AnaDataset
        tabular = {'plants':   ['fruit', 'fruit','fruit',   'fruit','vegetable','vegetable','vegetable','vegetable' ],
                   'quantity': ['1 kg' , '10 kg', '1 kg',   '10 kg',  '1 kg',    '10 kg',   '1 kg',     '10 kg'     ], 
                   'product':  ['apple', 'apple', 'orange', 'orange', 'peppers', 'peppers', 'carrot',   'carrot'    ], 
                   'price':    [1,       10,      2,        20,       1.5,       15,        0.5,        5           ]}
        analysis = AnaDataset(Sdataset.ntv(tabular).to_analysis(True))
        # `analysis` is also available from pandas data
        import pandas as pd
        import ntv_pandas as npd
        analysis = pd.DataFrame(tabular).npd.analysis()

In [2]: # each relationship is evaluated and measured 
        analysis.get_relation('plants', 'product').typecoupl
Out[2]: 'derived'

In [3]: analysis.get_relation('quantity', 'product').typecoupl
Out[3]: 'crossed'

In [4]: # the 'distance' between to Fields is measured (number of codec links to change to be coupled))
        analysis.get_relation('quantity', 'product').distance
Out[4]: 6

In [5]: # the dataset can be represented as a 'derived tree'
        print(analysis.tree())
Out[5]: -1: root-derived (8)
           1 : quantity (6 - 2)
           2 : product (4 - 4)
              0 : plants (2 - 2)
           3 : price (0 - 8)

In [6]: # 'partitions' are found (partitions are multi-dimensionnal data)'
        analysis.partitions(mode='id')
Out[6]: [['product', 'quantity'], ['price']]

In [7]: # the `field_partition` method return the main structure of the dataset
        analysis.field_partition(mode='id')
Out[7]: {'primary': ['quantity', 'product'],
         'secondary': ['plants'],
         'unique': [],
         'variable': ['price']}
```

## Uses

A TAB-analysis object is initialized by a set of properties (a dict with specific keys). It can therefore be used from any tabular data manager (e.g. pandas).

Possible uses are as follows:

- control of a dataset in relation to a data model,
- quality indicators of a dataset
- analysis of datasets

and in connection with the tabular application:

- error detection and correction,
- generation of optimized data formats
- interface to specific applications
