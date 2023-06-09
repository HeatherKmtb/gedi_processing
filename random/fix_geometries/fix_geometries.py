import rsgislib.vectorutils

rsgislib.vectorutils.check_validate_geometries('/bigdata/heather_gedi/layers/final_q.shp', 'final_q', '/bigdata/heather_gedi/layers/final_q.gpkg', 'final_q', out_format= 'GPKG', print_err_geoms= True, del_exist_vec= False)


