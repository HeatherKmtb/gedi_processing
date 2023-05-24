import glob
import rsgislib.imageutils.imagelut

img_list = glob.glob('/bigdata/copernicus-dem-30m/cop_30_slp_asp_tiles/cop_dem_30m_slope_tif/*.tif')
out_vec = '/bigdata/heather_gedi/data/1_deg_q/4.slope_lut.gpkg'
vec_lyr = 'slope'

rsgislib.imageutils.imagelut.create_img_extent_lut(img_list, out_vec, vec_lyr, out_format='GPKG', out_proj_wgs84 = True)



