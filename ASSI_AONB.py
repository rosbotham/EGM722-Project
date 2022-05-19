
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature

def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

Track = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Track_Centre.shp')
B_outline = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Binevenagh_C.shp')
Studya = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Study_Area.shp')
Gazetteer = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Gazetteer_C.shp')
Census = gpd.read_file('C:\\Users\\Aaron\\Documents\\GitHub\\EGM722-Project\\Dataset_files\\census_areas.shp')
Roads = gpd.read_file('C:\\Users\\Aaron\\Documents\\GitHub\\EGM722-Project\\Dataset_files\\clipped_roads.shp')
AONB = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\AONB_C.shp')
ASSI = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\ASSI.shp')

fig = plt.figure(figsize=(10, 10))
mycrs = ccrs.epsg(29902)
ax = plt.axes(projection=ccrs.PlateCarree())
outline_feature = ShapelyFeature(Studya['geometry'], mycrs, edgecolor='k', facecolor='none')
xmin, ymin, xmax, ymax = Studya.total_bounds
ax.add_feature(outline_feature)
""" Creates a 10x10 inch map.
Sets the CRS to 29902. CRS is set to TM65 Irish Grid where the study area is located. 
Converts units from degrees to metres (M) to carry out analysis.
Constrains the map to the area of interest to allow for a close up image of the study area.
"""

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
"""Creates the scale bar for the map and positions it at the bottom of the figure. 
Scale bar is divided up into 5km, 10km and 20km."""

Binevenagh_feat = ShapelyFeature(B_outline['geometry'],  mycrs, edgecolor='black', facecolor='whitesmoke', linewidth=1)
ax.add_feature(Binevenagh_feat)
ax.plot(Gazetteer.geometry.x, Gazetteer.geometry.y, marker='d', markersize='3.5', linestyle='',
        color='c', transform=mycrs)
"""Plots datasets containing towns within the area 
and the outline of the study area"""

for i, row in Gazetteer.iterrows():
    x, y = row.geometry.x, row.geometry.y # get the x,y location for each town
    plt.text(x, y, row['NAME'].title(), fontsize=8, transform=mycrs) # use plt.text to place a label at x,y
"""Plots text labels for town names from gazetteer file. Uses x and y coordinates to plot town names according to 
their coordinates."""

AONB_feat = ShapelyFeature(AONB['geometry'], mycrs, facecolor='purple', edgecolor='black')
ax.add_feature(AONB_feat)
ASSI_feat = ShapelyFeature(ASSI['geometry'], mycrs, facecolor='pink', edgecolor='black')
ax.add_feature(ASSI_feat)
"""Plots AONB and ASSI datasets onto the map"""
ax.plot(Track.geometry.x, Track.geometry.y, marker='o', markersize='3.5', linestyle='', color='green', transform=mycrs)
Trackbuffer = Track['geometry'].buffer(distance=1000)
Trackbuffer.plot
"""Plots the track point and generates a buffer surrounding the track in metres. A buffer of 1000m has been selected, 
however this can be changed to whichever distance is required."""


ASSI_buff = (Trackbuffer.contains(ASSI['geometry']))
print(ASSI_buff.head)
"""Identifies the amount of ASSIs that are contained within the buffer area."""

# Create Handles for datasets
AONBHandle = generate_handles(['AONBs'], ['purple'])
ASSIHandle = generate_handles(['ASSIs'], ['pink'])
TownHandle = generate_handles(['Towns'],  ['c'])
TrackHandle = generate_handles(['Track'], ['green'])
handles = AONBHandle + ASSIHandle + TownHandle + TrackHandle
labels = ['AONBs', 'ASSIs', 'Towns', 'Track',]
leg = ax.legend(handles,  labels, title='Legend', title_fontsize=14,
        fontsize=12, loc='upper left', frameon=True, framealpha=1)
"""
Creates the handles for each dataset used and is added to the legend that is used within the map.
Handles include:
ASSIs within Binevenagh 
AONBs within Binevenagh
Gazetteer
Track centre
Adds legend to the top left of the map 
"""

scale_bar(ax)
"""adds the scale bar to the map"""

fig.savefig('C:\\GitHub\\EGM722-Project\\assi_aonb_map.png', bbox_inches='tight', dpi=300)
"""saves the map as a png file with 300 dots per inch"""