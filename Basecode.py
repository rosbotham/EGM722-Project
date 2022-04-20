import pandas as pd
import csv
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from shapely.geometry import Point, LineString, Polygon


#Datasets
StudyA = gpd.read_file(r'C:\GitHub\EGM722-Project\data_files\Binevenagh_Clip.shp')
Gazetteer = gpd.read_file(r'C:\GitHub\EGM722-Project\data_files\Clipped_Gazateer.shp')
AONB = gpd.read_file('C:\GitHub\EGM722-Project\data_files\AONB_Clip.shp')
ASSI = gpd.read_file('C:\GitHub\EGM722-Project\data_files\ASSI_Clip.shp')
Roads = gpd.read_file('C:\GitHub\EGM722-Project\data_files\clipped_roads.shp')
BinB = pd.read_csv('C:\GitHub\EGM722-Project\data_files\Binevenagh_Point.csv')
print(BinB)
#convert Binevenagh into Geodataframe
BinB_GDF = gpd.GeoDataFrame(BinB, geometry = gpd.points_from_xy(BinB['X'], BinB['Y']))
print(BinB_GDF)


#Create Motorbike Track Point
Track = Point(24400, 433580)
Track_buffer = Track.buffer(1)

print(Gazetteer)
