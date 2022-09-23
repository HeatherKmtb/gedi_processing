import rsgislib
import rsgislib.vectorutils
import rsgislib.vectorutils.createvectors
import rsgislib.vectorattrs

glb_tiles_vec_file = "/scratch/a.hek4/gedi_processing/glb_land_roi_deg_tiles_named.geojson"
glb_tiles_vec_lyr = "grid"
glb_land_vec_file = "/scratch/a.hek4/gmw/gmw_v3_2020_vec.shp"
glb_land_vec_lyr = "level0"

glb_land_tiles_vec_file = "glb_land_roi_deg_tiles_named.geojson"
glb_land_tiles_vec_lyr = "glb_land_roi_deg_tiles_named"


rsgislib.vectorattrs.create_name_col(glb_land_roi_tiles_vec_file, glb_land_roi_tiles_vec_lyr,
                                     glb_land_roi_tiles_named_vec_file, glb_land_roi_tiles_named_vec_lyr,
                                     out_format='GeoJSON', out_col='tile_name', x_col='xmin', y_col='ymax',
                                     prefix='gedi_', coords_lat_lon=True, int_coords=True, zero_x_pad=3, zero_y_pad=2,
                                     round_n_digts=0, non_neg=True)

