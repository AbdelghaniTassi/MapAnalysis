import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-i', '--pointsLayer', required=True)
    parser.add_argument('-r', '--polygonsLayer', required=True)
    parser.add_argument('-a', '--attributeStats', required=True)
    args = parser.parse_args()
    
    print (args)
    
