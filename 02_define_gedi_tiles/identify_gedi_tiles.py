import rsgislib
import rsgislib.vectorutils
import rsgislib.vectorutils.createvectors
import rsgislib.vectorattrs

glb_tiles_vec_file = "/bigdata/petebunting/Dropbox/University/Research/Data/World/Global_1d_grid.gpkg"
glb_tiles_vec_lyr = "grid"
glb_land_vec_file = "/bigdata/petebunting/Dropbox/University/Research/Data/World/GADM_Boundaries/gadm36_levels.gpkg"
glb_land_vec_lyr = "level0"

glb_land_tiles_vec_file = "glb_land_deg_tiles.geojson"
glb_land_tiles_vec_lyr = "glb_land_deg_tiles"

rsgislib.vectorutils.spatial_select(glb_tiles_vec_file, glb_tiles_vec_lyr, glb_land_vec_file, glb_land_vec_lyr,
                                    out_vec_file, out_vec_lyr, out_format='GeoJSON')


gedi_roi_vec_file = "gedi_glb_roi.geojson"
gedi_roi_vec_lyr = "gedi_glb_roi"
bboxs = [[-180, 180, -54, 54]]
rsgislib.vectorutils.createvectors.create_poly_vec_bboxs(gedi_roi_vec_file, gedi_roi_vec_lyr, "GeoJSON", 4326, bboxs)

glb_land_roi_tiles_vec_file = "glb_land_roi_deg_tiles.geojson"
glb_land_roi_tiles_vec_lyr = "glb_land_roi_deg_tiles"

rsgislib.vectorutils.spatial_select(glb_land_tiles_vec_file, glb_land_tiles_vec_lyr, gedi_roi_vec_file, gedi_roi_vec_lyr,
                                    glb_land_roi_tiles_vec_file, glb_land_roi_tiles_vec_lyr, out_format='GeoJSON')

rsgislib.vectorattrs.pop_bbox_cols(glb_land_roi_tiles_vec_file, glb_land_roi_tiles_vec_lyr, x_min_col='xmin',
                                   x_max_col='xmax', y_min_col='ymin', y_max_col='ymax')

glb_land_roi_tiles_named_vec_file = "glb_land_roi_deg_tiles_named.geojson"
glb_land_roi_tiles_named_vec_lyr = "glb_land_roi_deg_tiles_named"

rsgislib.vectorattrs.create_name_col(glb_land_roi_tiles_vec_file, glb_land_roi_tiles_vec_lyr,
                                     glb_land_roi_tiles_named_vec_file, glb_land_roi_tiles_named_vec_lyr,
                                     out_format='GeoJSON', out_col='tile_name', x_col='xmin', y_col='ymax',
                                     prefix='gedi_', coords_lat_lon=True, int_coords=True, zero_x_pad=3, zero_y_pad=2,
                                     round_n_digts=0, non_neg=True)

