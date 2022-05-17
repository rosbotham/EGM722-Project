"""Program that maps Binevenagh area to aid in planning approval.
This script is designed to create a Landcover map of the study area.
These will be used to identify potential impact of the track on
the surrounding biodiversity
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs


def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


Track = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Track_Centre.shp')
B_outline = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Binevenagh_C.shp')
Studya = gpd.read_file('C:\\GitHub\\EGM722-Project\\Dataset_files\\Study_Area.shp')
Landcover = gpd.read_file('C:\\Users\\Aaron\\Documents\\GitHub\\EGM722-Project\\Dataset_files\\NW_coast_Land_Cover.shp')


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
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = (lly1 + lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx - 10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby - 4000, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx - 12500, sby - 4000, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx - 18500, sby - 4000, '5km', transform=tmc, fontsize=8)


"""Creates the scale bar for the map and positions it at the bottom of the figure. Divided up into 5km, 10km and 20km.
"""

Binevenagh_feat = ShapelyFeature(B_outline['geometry'], mycrs, edgecolor='black', facecolor='whitesmoke')
ax.add_feature(Binevenagh_feat)


# get the number of unique BHSUB codes in the dataset
num_BHSUB = list(Landcover.BHSUB.unique())
print('Number of unique features: {}'.format(num_BHSUB))
BHSUB_colors = ['darkolivegreen', 'olivedrab', 'olive', 'yellowgreen', 'greenyellow', 'chartreuse', 'lawngreen',
                'darkseagreen', 'lightgreen', 'limegreen', 'sienna', 'royalblue', 'peru', 'brown', 'gray', 'grey',
                'dimgrey', 'dimgray', 'darkslateblue', 'blue']

for i, name in enumerate(Landcover):
    Landcoverf = ShapelyFeature(Landcover['geometry'], mycrs,
                                edgecolor='black',
                                facecolour=BHSUB_colors[i],
                                linewidth=1,
                                alpha=0.25)
ax.add_feature(Landcoverf)
print(Landcoverf)
"""Adds the land cover data to the map.
Identifies how many unique land cover types are contained in the shapefile. 
Gives each land cover type a unique colour code and adds shapefile to the map."""


ax.plot(Track.geometry.x, Track.geometry.y, marker='o', markersize='3.5', linestyle='', color='orange', transform=mycrs)
Trackbuffer = Track.buffer(1000)  # Distance is in M as we are using Irish Grid.
print(type(Trackbuffer))
"""Plots the track point and generates a buffer surrounding the track"""

# stats
# count of land cover polygons within the buffer
# sum area of landcover
Landb= (Trackbuffer.contains(Landcover, align=True))
print(Landb.values[1])


# Create Handles for datasets
LandcoverHandle = generate_handles(Landcover.BHSUB.unique(), color=BHSUB_colors, alpha=0.25)
TownHandle = generate_handles(['Towns'],  ['c'])
TrackHandle = generate_handles(['Track'], ['orange'])
handles = LandcoverHandle + TownHandle + TrackHandle
labels = ['Landcover type', 'Towns', 'Track']
leg = ax.legend(handles,  labels, title='Legend', title_fontsize=14,
                fontsize=12, loc='upper left', frameon=True, framealpha=1)
"""Creates handles for datasets to be used for the map's legend"""

scale_bar(ax)
"""adds the scale bar to the map"""
fig.savefig('C:\\Users\\Aaron\\Documents\\GitHub\\EGM722-Project\\Ecology_map.png',
            bbox_inches='tight', dpi=300)
"""saves the map as a png file with 300 dots per inch"""
