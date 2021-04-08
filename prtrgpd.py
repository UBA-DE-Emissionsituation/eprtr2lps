#small function to convert the lps csv output to a shapefile for GIS Display and Work
import geopandas as gpd
import pandas as pd

def convert_output_to_shp(input,delimit='|',header=0):
    data=pd.read_csv(input,delimiter=delimit,header=0,encoding='utf8')
    bname=input.split('.')[0]
    locations=gpd.GeoDataFrame(data,geometry=gpd.points_from_xy(data['Longitude (deg)'],data['Latitude (deg)']),crs='epsg:4326')#watch out for the Lat Long kwds
    locations.to_file(bname+'_pts.shp',encoding='utf8')
    return None