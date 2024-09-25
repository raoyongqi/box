import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import numpy as np

#Function for plotting tick marks
def cartopy_plot_tickmarks(ax,labels,axis):
    
    assert axis in ['x','y']

    ticks=[]
    values=[float(txt.get_text().split('°')[0]) for txt in labels]
    directions=[txt.get_text().split('°')[1] for txt in labels]  #what comes after the degree symbol
    for i,txt in enumerate(labels):
        value=values[i]
        if directions[i] in ['W','S']:
            ticks+=[-value]
        else:  #for 'E', 'N' and '' (e.g. 180 degrees)
            ticks+=[value]
    
    if axis=='x':
        ax.set_xticks(ticks, crs=ccrs.PlateCarree())
        ax.set_xticklabels(['' for i in range(len(ticks))])  #make new ticks have blank labels to not overplot cartopy's
    elif axis=='y':
        ax.set_yticks(ticks, crs=ccrs.PlateCarree())
        ax.set_yticklabels(['' for i in range(len(ticks))])

        
proj=ccrs.PlateCarree(central_longitude=45)  #to show this working for a non-zero central_longitude
nrows=2
ncolumns=2
fig, axarr = plt.subplots(nrows, ncolumns, figsize=(10, 6), subplot_kw={'projection':proj})

#Making plots and adding cartopy labels to left and bottom panels
for i in range(nrows*ncolumns):
    row_ind=i//ncolumns
    col_ind=i%ncolumns
    ax=axarr[row_ind, col_ind]
    ax.coastlines()
    ax.set_extent([-100,100,-45,70], proj)  #just to show it working with axes different from the default
    draw_labels=[]
    if row_ind==nrows-1:
        draw_labels+=['bottom']
    if col_ind==0:
        draw_labels+=['left']

    gl=ax.gridlines(draw_labels=draw_labels)
    gl.xlines = False  #removing gridlines
    gl.ylines = False
    if row_ind==nrows-1 and col_ind==0:  #saving gridliner that has both left and bottom labels for getting tick values below
        gl_save=gl

    lon_formatter = LongitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    lat_formatter = LatitudeFormatter()
    ax.yaxis.set_major_formatter(lat_formatter)

#getting the cartopy tick information
plt.draw()  
xlabels=gl_save.xlabel_artists
ylabels=gl_save.ylabel_artists

#adding tick marks at label locations
for i in range(nrows*ncolumns):
    row_ind=i//ncolumns
    col_ind=i%ncolumns
    ax=axarr[row_ind, col_ind]
    
    cartopy_plot_tickmarks(ax,xlabels,'x')
    cartopy_plot_tickmarks(ax,ylabels,'y')

fig.subplots_adjust(hspace=0.05, wspace=0.05)  #removing whitespace

plt.show()