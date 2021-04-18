"""small function to convert the lps csv output to a shapefile for GIS Display and Work"""
import geopandas as gpd
import pandas as pd


def convert_output_to_shp(inputt, delimit='|', header=0):
    data = pd.read_csv(inputt, delimiter=delimit, header=header, encoding='utf8')
    filename = inputt.split('.')[0]
    locations = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['Longitude (deg)'], data['Latitude (deg)']), crs='epsg:4326')
    # watch out for the Latitude Longitude Keywords in your pandas frame
    locations.to_file(filename + '_pts.shp', encoding='utf8')
    return None
