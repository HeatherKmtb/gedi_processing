singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif \
rsgisbuildimglut.py -i "/scratch/a.hek4/srtm/srtm_raw_tiles/extracted/*.hgt" \
-o /scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_tiles_prod_imgs_lut.gpkg \
--veclyr srtm_lut --vecformat GPKG --overwrite

singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif \
rsgisbuildimglut.py -i "/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_aspect_tiles/*.kea" \
-o /scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_tiles_prod_imgs_lut.gpkg \
--veclyr aspect_lut --vecformat GPKG

singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif \
rsgisbuildimglut.py -i "/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_slope_tiles/*.kea" \
-o /scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_tiles_prod_imgs_lut.gpkg \
--veclyr slope_lut --vecformat GPKG
