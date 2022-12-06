singularity exec --bind /bigdata:/bigdata --bind /home/heather:/home/heather /bigdata/heather_gedi/sw_image/au-eoed-dev.sif rsgischkgdalfile.py -i "/bigdata/heather_gedi/data/1_deg_q/2.join_lc/GEDI02_B_2020_Q1/*.gpkg" --vec --rmerr --printerr --epsg 4326 --chkproj

