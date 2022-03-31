find /scratch/a.hek4/srtm/srtm_raw_tiles/extracted -type f > srtm_raw_files.txt

singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif  gdalbuildvrt -srcnodata "-32768" -vrtnodata "-32768" -input_file_list srtm_raw_files.txt /scratch/a.hek4/gedi_files_2021_12_16/data/srtm_global_mosaic_1arc_v3.vrt

