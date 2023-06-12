singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif rsgischkgdalfile.py -i "/scratch/a.hek4/data/1_deg_q/3.remove_lc_cats/GEDI02_B_2021_Q3/*.gpkg" --vec --rmerr --printerr --epsg 4326 --chkproj

