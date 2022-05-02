"""Program that maps Binevenagh area to aid in planning approval.

This program is designed to map out the study area of Binevenagh where a motorbike track has been sent for approval.
It includes shapefiles that have been clipped to the study area e.g. AONBs, ASSIs, Roads and Gazetteer.
Additionally, CSV files will be used and converted to GeoDataFrames and Shapely Geometry types such as
points will be created.
"""
import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import cartopy.mpl.geoaxes
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
from shapely.geometry import Point

plt.ion()






"""Datasets that have been imported are:
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
# Datasets needed for practical
Buildings = pd.read_csv('C:\\GitHub\\EGM722-Project\\Dataset_files\\Binevenagh_Point.csv')
Track = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Track_Centre.shp')
B_outline = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Binevenagh_C.shp')
Studya = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Study_Area.shp')
Gazetteer = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Gazetteer_C.shp')
Census = gpd.read_file('C:\\Users\\Aaron\\Documents\\GitHub\\EGM722-Project\\Dataset_files\\Pop_density.shp')


"""Here is where the dimensions for the map are written. The map produced will be 10x10 inches long. 
The crs is set Irish Grid which will allow user to carry out analysis using metres (M).
The figure is constrained to the area of interest to allow for a close up image of the study area.
"""
fig = plt.figure(figsize=(10, 10))
mycrs = ccrs.epsg(29902)
ax = plt.axes(projection=ccrs.PlateCarree())
outline_feature = ShapelyFeature(Studya['geometry'], mycrs, edgecolor='k', facecolor='none')
xmin, ymin, xmax, ymax = Studya.total_bounds
ax.add_feature(outline_feature)

def scale_bar(ax, location=(0.9, 0.03)):
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


"""Next, the datasets containing the roads in the area, towns within the area 
and the outline of the study area are added to the map"""
# Roads_feat = ShapelyFeature(Roads['geometry'], mycrs, linestyle='-', color='grey')
# ax.add_feature(Roads_feat)
#ax.plot(Roads.geometry, linestyle='-',  color='grey', transform=mycrs)

Binevenagh_feat = ShapelyFeature(B_outline['geometry'],  mycrs, edgecolor='black', facecolor='whitesmoke', linewidth=1)
ax.add_feature(Binevenagh_feat)
"""The Gazetteer shapefile is then plotted to identify towns within the area"""
ax.plot(Gazetteer.geometry.x, Gazetteer.geometry.y, marker='d', markersize='3.5', linestyle='',
        color='c', transform=mycrs)
"""Next the town names from the Gazetteer file are added to the map"""
for i, row in Gazetteer.iterrows():
    x, y = row.geometry.x, row.geometry.y # get the x,y location for each town
    plt.text(x, y, row['NAME'].title(), fontsize=8, transform=mycrs) # use plt.text to place a label at x,y


"""A colour bar is used to illustrate the population density within the Binevenagh Area with purple for low population 
density and yellow for high population density"""
# colorbar to illustrate population density:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)
PopnDens_plot = Census.plot(column='POPDN', ax=ax, transform=mycrs, vmin=0, vmax=700, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

"""The dataset that contains information on the buildings within the Binevenagh area is then converted from tabular
data into a Geodataframe to display the geography of the points"""
# Convert Binevenagh Buildings table into Geodataframe
Buildings.head()
Buildings['geometry'] = list(zip(Buildings['X'], Buildings['Y']))
Buildings['geometry'] = Buildings['geometry'].apply(Point)
Buildgdf = gpd.GeoDataFrame(Buildings)
Buildgdf.set_crs("EPSG:29902", inplace=True)
BinBs = ax.plot(Buildgdf.geometry.x,
                Buildgdf.geometry.y, marker='*', markersize='3.5', linestyle='', color='red', transform=mycrs)

"""The next step is to add the track point to the map. From here, a buffer can be generated to be used in the
 spatial analysis part of the script. A buffer of 1000m has been selected, however this can be changed to whichever
  distance is required. 
  As noise complaints have been made from 1km-2km away from the site a buffer will be made for both of these distances 
  to identify how many buildings will be affected by the track"""

ax.plot(Track.geometry.x, Track.geometry.y, marker='o', markersize='3.5', linestyle='', color='yellow', transform=mycrs)
Trackbuffer = Track.buffer(1000)  # Distance is in M as we are using Irish Grid.
print(type(Trackbuffer))

#Point.distance(Track, BinBs)
# Check CRS is all standard Irish Grid
print("Binevenagh_outline", Buildgdf.crs)
print("Binevenagh Buildings", Buildgdf.crs)
print("Gazetter", Gazetteer.crs)
# print("Roads", Roads.crs)

"""This function has been created to identify the amount of residential buildings within the buffer area."""
ResB = Buildgdf.to_crs(epsg=29902)  # This creates a new class that we can use for our analysis
ResB[ResB['USE'] == 'RESIDENTIAL']  # Only residential buildings are selected
#Resbuff = gpd.sjoin(ResB, Trackbuffer)
#Res1 = (Trackbuffer.contains(ResB))
#print(Res1.values[1])

"""This function is created to identify the amount of commercial buildings within the buffer"""
Commercial = Buildgdf.to_crs(epsg=29902)
Commercial[Commercial['USE'] == 'COMMERCIAL']
#Com1 = (Trackbuffer.contains(Commercial, align=True))
#print(Com1.values[1])

"""
This function creates the handles for the legend that is used within the map
"""

def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# Create Handles for datasets
NI_OLHandle = generate_handles(['NI Outline'], ['whitesmoke'])
GazeHandle = generate_handles(['Gazetteer'], ['c'])
BinBHandle = generate_handles(['Buildings'], ['red'])
TrackHandle = generate_handles(['Track Centre'], ['yellow'])

handles = NI_OLHandle + GazeHandle + BinBHandle + TrackHandle
labels = ['NI Outline', 'Gazetteer', 'Buildings', 'Track Centre']
leg = ax.legend(handles,  labels, title='Legend', title_fontsize=14, fontsize=12, loc='upper left', frameon=True,
                framealpha=1)


#scale_bar(ax)
fig.savefig('C:\\GitHub\\EGM722-Project\\social_map.png', bbox_inches='tight', dpi=300)