
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
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

def scale_bar(ax, location=(0.9, 0.03), length =10000):
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
Roads_feat = ShapelyFeature(Roads['geometry'], mycrs, linestyle='-', color='grey')
ax.add_feature(Roads_feat)
Binevenagh_feat = ShapelyFeature(B_outline['geometry'],  mycrs, edgecolor='black', facecolor='whitesmoke', linewidth=1)
ax.add_feature(Binevenagh_feat)
ax.plot(Gazetteer.geometry.x, Gazetteer.geometry.y, marker='d', markersize='3.5', linestyle='',
        color='c', transform=mycrs)
"""Next the town names from the Gazetteer file are added to the map"""
for i, row in Gazetteer.iterrows():
    x, y = row.geometry.x, row.geometry.y # get the x,y location for each town
    plt.text(x, y, row['NAME'].title(), fontsize=8, transform=mycrs) # use plt.text to place a label at x,y
AONB_feat = ShapelyFeature(AONB['geometry'], mycrs, facecolor='purple', edgecolor='black')
ax.add_feature(AONB_feat)
ASSI_feat = ShapelyFeature(ASSI['geometry'], mycrs, facecolor='pink', edgecolor='black')
ax.add_feature(ASSI_feat)


"""The next step is to add the Tack point dataset to the map. From here, a buffer can be generated to be used in the
spatial analysis part of the script. A buffer of 1000m has been selected, however this can be changed to whichever
distance is required"""

ax.plot(Track.geometry.x, Track.geometry.y, marker='o', markersize='3.5', linestyle='', color='green', transform=mycrs)
Trackbuffer = Track['geometry'].buffer(distance=1000)
# = Track.buffer(2000)
Trackbuffer.plot

"""This function has been created to identify the amount of ASSIs within the buffer area."""
ASSI_buff = (Trackbuffer.contains(ASSI['geometry']))
print(ASSI_buff.head)

# Create Handles for datasets
AONBHandle = generate_handles(['AONBs'], ['purple'])
ASSIHandle = generate_handles(['ASSIs'], ['pink'])
TownHandle = generate_handles(['Towns'],  ['c'])
TrackHandle = generate_handles(['Track'], ['green'])

handles = AONBHandle + ASSIHandle + TownHandle + TrackHandle
labels = ['AONBs', 'ASSIs', 'Towns', 'Track',]
leg = ax.legend(handles,  labels, title='Legend', title_fontsize=14,
        fontsize=12, loc='upper left', frameon=True, framealpha=1)
scale_bar(ax)

fig.savefig('C:\\GitHub\\EGM722-Project\\assi_aonb_map.png', bbox_inches='tight', dpi=300)
