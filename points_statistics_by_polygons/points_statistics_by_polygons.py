import argparse
from geopandas.tools import sjoin
import geopandas as gpd
import pandas as pd


def execute(pointsLayer, polygonsLayer, attributeStats, output):
    # read points file
    points = gpd.read_file(pointsLayer)

    # read polygons file
    polygons = gpd.read_file(polygonsLayer)
    print(polygons)
    
    # join points with polygons
    points_polys = gpd.sjoin(points, polygons, how="left")
    print (points_polys)

    # compute statistics
    stats_pt = points_polys.groupby('index_right')[attributeStats].agg(['mean','count','max','min'])
    print (stats_pt)

    # merge stats with polygons layer
    result = pd.concat([polygons, stats_pt], axis=1)
    print (result)

    # write result to output file
    result.to_file(output)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-i', '--pointsLayer', required=True)
    parser.add_argument('-r', '--polygonsLayer', required=True)
    parser.add_argument('-a', '--attributeStats', required=True)
    args = parser.parse_args()
    print (args)
    # launch algorithm
    execute(args.pointsLayer, args.polygonsLayer, args.attributeStats, args.output)
    
