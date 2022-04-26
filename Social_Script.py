"""Program that maps Binevenagh area to aid in planning approval.

This program is designed to map out the study area of Binevenagh where a motorbike track has been sent for approval.
It includes shapefiles that have been clipped to the study area e.g. AONBs, ASSIs, Roads and Gazetteer.
Additionally, CSV files will be used and converted to GeoDataFrames and Shapely Geometry types such as
points will be created.
These will be used by the program to cary out several functions such as buffers,
"""
import csv
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
from shapely.geometry import Point, Polygon, box, multipoint
import numpy as np
import fiona


plt.ion()

def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

def scale_bar(ax, location=(0.8, 0.05)):
    llx0,  llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = (lly1 + lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0,  x1,  y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx - 10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby - 4000, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx - 12500, sby - 4000, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx - 18500, sby - 4000, '5km', transform=tmc, fontsize=8)
    plt.text(sbx - 24500, sby - 4000, '0 km', transform=tmc, fontsize=8)


# Datasets needed for practical
NI_outline = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\NI_outline.shp')
Studya = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\study_area_box.shp')
Gazetteer = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Clipped_Gazateer.shp')
Roads = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\clipped_roads.shp')
Bin = pd.read_csv('C:\\GitHub\\EGM722-Project\\Dataset_files\\Binevenagh_Point.csv')
"""Datasets Imported are
1. Outline of NI
2. Study Area of the assessment
3. Towns within NI
4.  Roads within NI
5. Table containing information on buildings within Binevenagh area  
    Attributes:
    Building number
    Road
    Type of building
    X coordinates
    Y coordinates
   ."""
myFig = plt.figure(figsize=(10, 10))
myCRS = ccrs. UTM(29) # Ireland situated in UTM29
ax = plt.axes(projection=ccrs.Mercator())
outline_feature = ShapelyFeature(Studya['geometry'], myCRS, edgecolor='k', facecolor='none')
xmin, ymin, xmax, ymax = Studya.total_bounds
ax.add_feature(outline_feature)

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False

# colorbar to illustrate population density:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)
NI_OL = ShapelyFeature(NI_outline['geometry'], crs=myCRS, edgecolor='black', facecolor='none')
ax.add_feature(NI_OL)

#Clip NI shapefile to
NI_Clip = []
tmp_clip = gpd.clip(NI_outline, Studya)
NI_Clip.append(tmp_clip)


# Convert Binevenagh Buildings table into Geodataframe
Bin.head()
Bin['geometry'] = list(zip(Bin['X'], Bin['Y']))
Bin['geometry'] = Bin['geometry'].apply(Point)
Bingdf = gpd.GeoDataFrame(Bin)
Bingdf.set_crs("EPSG:29902", inplace=True)
BinBs = ax.plot(Bingdf.geometry.x, Bingdf.geometry.y, marker='*', color='red', transform=myCRS)

print(Gazetteer)
ax.plot(Gazetteer.geometry.x, Gazetteer.geometry.y, marker='d', color='c', transform=myCRS)

# Check CRS is all standard Irish Grid
print("NI_outline", NI_outline.crs)
print("Studya", Studya.crs)
print("Gazetter", Gazetteer.crs)
print("Roads", Roads.crs)

# Create Motorbike Track Point
# Create Motorbike Track Point
Track = Point(388166, 6109381)
ax.plot(Track, marker='o', transform=myCRS)

Track_buffer = Track.buffer(1000)
print(type(Track_buffer))


#Identify how many residents are in track area
Resneartrk = gpd.overlay(BinBs, Track_buffer, how='intersection')


# Create Handles for datasets
NI_OLHandle = generate_handles(['NI Outline'], ['whitesmoke'])
GazeHandle = generate_handles(['Gazetteer'], ['c'])
BinBHandle = generate_handles(['Buildings'], ['red'])
TrackHandle = generate_handles(['Track Centre'], ['blue'])

handles = NI_OLHandle + GazeHandle + BinBHandle + TrackHandle
labels = ['NI Outline', 'Gazetteer', 'Buildings', 'Track Centre']
leg = ax.legend(handles,  labels, title='Legend', title_fontsize=14,
        fontsize=12, loc='upper left', frameon=True, framealpha=1)


scale_bar(ax)
myFig.savefig('C:\GitHub\EGM722-Project\Images\social_map.png', bbox_inches='tight', dpi=300)
