import glob
import rsgislib.tools.checkdatasets

vec_files = glob.glob(
    "/scratch/a.hek4/gedi_files_2021_12_16/data/gedi_orbits_tiled/*.gpkg"
)

rsgislib.tools.checkdatasets.run_check_gdal_vector_files(
    vec_files,
    chk_proj=True,
    epsg_code=4326,
    rm_err=True,
    print_err=True,
    multi_file=False,
    print_file_names=False,
    timeout=4,
)
