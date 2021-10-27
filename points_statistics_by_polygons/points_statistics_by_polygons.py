import argparse
from geopandas.tools import sjoin
import geopandas as gpd

def execute(pointsLayer, polygonsLayer, attributeStats, output):
    # read points file
    points = gpd.read_file(pointsLayer)
    # read polygons file
    polygons = gpd.read_file(polygonsLayer)
    # join points with polygons
    points_polys = gpd.sjoin(points, polygons, how="left")
    # compute statistics
    stats_pt = points_polys.groupby('id_right')[attributeStats].agg(['mean','std','max','min'])
    # merge stats with polygons layer
    result = pd.merge(polygons, stats_pt , left_on='id',right_index=True,how='outer')

    print (output)
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
    
