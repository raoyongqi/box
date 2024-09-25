import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

#ref: https://scitools.org.uk/cartopy/docs/latest/gallery/gridlines_and_labels/gridliner.html#sphx-glr-gallery-gridlines-and-labels-gridliner-py
rotated_crs = ccrs.RotatedPole(pole_longitude=120.0, pole_latitude=70.0)
fig = plt.figure(figsize=(12,6))


# non-gridlines
ax1 = fig.add_subplot(1,2,2, projection=rotated_crs)
ax1.set_extent([-6, 1, 47.5, 51.5], crs=ccrs.PlateCarree())
ax1.add_feature(cfeature.LAND.with_scale('110m'))
ax1.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False,color = "None")
ax1.set_title('Non-gridlines',fontsize = 24)
plt.savefig("grid.png")