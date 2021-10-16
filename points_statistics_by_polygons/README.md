# Points statistics by polygons
## Overview

![](https://i.stack.imgur.com/Di39x.png)

First of all it is necessary to determine the points that are contained in the polygons and which points in which polygons

```python
points = gpd.read_file("points.shp")
points.head()
   id  value1 value2    geometry
0   1   300   300003    POINT (19.579 -18.625)
1   2   400   400003    POINT (80.639 -114.895)
2   3   500   500003    POINT (98.021 -70.326)
3   4   100   100003    POINT (118.522 -100.187)
4   5   200   200003    POINT (186.713 -35.562)
polys = gpd.read_file("polys.shp")
polys
   id     geometry
0   1   POLYGON ((51.223 -134.951, 50.777 -74.337, 106...
1   2   POLYGON ((223.706 -134.506, 228.163 -68.543, 3...
2   3   POLYGON ((151.058 -185.315, 167.994 -167.487, ...
```
Use a spatial join (as in More Efficient Spatial join in Python without QGIS, ArcGIS, PostGIS, etc for example)

```python
from geopandas.tools import sjoin
points_polys = gpd.sjoin(points, polys, how="left")
points_polys.head()
 id_left value1 value2      geometry         index_right  id_right
0   1     300   300003  POINT (19.579 -18.625)  NaN        NaN
1   2     400   400003  POINT (80.639 -114.895) 0.0        1.0
2   3     500   500003  POINT (98.021 -70.326)  0.0        1.0
3   4     100   100003  POINT (118.522 -100.187)0.0        1.0
4   5     200   200003  POINT (186.713 -35.562) NaN        NaN
```

The points id 1,2,3 are contained in the polygon 1 (id_right), etc...
Control of the number of points contained in the polygons 


```python
print(points_polys.loc[points_polys.id_right == 1,'value1'].count())
3
print(points_polys.loc[points_polys.id_right == 2,'value1'].count())
2
print(points_polys.loc[points_polys.id_right == 3,'value1'].count())
6
```
To summarize the stats for each attribute in the point layer and add it to the polygon layer, group the points_polys by the id_right column (= polygons) and compute the mean, standard deviation, max and min of the attributes of each group of points (Naming returned columns in Pandas aggregate function)

```python
stats_pt = points_polys.groupby('id_right')['value1','value2'].agg(['mean','std','max','min'])
stats_pt.columns = ["_".join(x) for x in result.columns.ravel()] # 
stats_pt 

        value1_mean value1_std value1_max value1_min value2_mean    value2_std    value2_max value2_min
id_right                                
1.0     333.333333  208.166600   500       100      333336.333333   208166.599947   500003    100003
2.0     735.000000   91.923882   800       670      735003.000000   91923.881554    800003    670003
3.0     36.333333    19.459359   60          7      36336.333333    19459.359359    60003       7003

```

It is also possible to use Named aggregations (Pandas in 2019 - let's see what's new!)

```python
stats_pt  = points_polys.groupby('id_right').agg( 
       value1_mean = ('value1','mean'),
       value1_std  = ('value1','std'),
       value1_max  = ('value1','max'),
       value1_min  = ('value1','min'),
       value2_mean = ('value2','mean'),
       value2_std  = ('value2','std'),
       value2_max  = ('value2','max'),
       value1_min  = ('value2','min'))

Finally join this DataFrame to the polygon GeoDataFrame and save the resulting layer

import pandas as pd
result = pd.merge(polys, stats_pt , left_on='id',right_index=True,how='outer')
result
   id                   geometry               value1_mean  value1_std  value1_max  value1_min  value2_mean   value2_std      value2_max value2_min
 0  1   POLYGON ((51.223 -134.951, 50.77...     333.333333  208.166600    500         100       333336.333333   208166.599947 500003    100003
 1  2   POLYGON ((223.706 -134.506, 228.16...   735.000000  91.923882     800         670       735003.000000   91923.881554  800003    670003
 2  3   POLYGON ((151.058 -185.315, 167.99...   36.333333   19.459359      60           7       36336.333333    19459.359359  60003       7003


 result.to_file("stat_point_poly.shp")

```

With value1_std as label:


![](https://i.stack.imgur.com/bKotf.png)

