import glob
import os

import tqdm
import rsgislib.tools.utils
import rsgislib.vectorattrs

tiles_vec_file='../glb_land_roi_deg_tiles_named.geojson'
tiles_vec_lyr='glb_land_roi_deg_tiles_named'

tile_names = rsgislib.vectorattrs.read_vec_column(tiles_vec_file, tiles_vec_lyr, att_column='tile_name')

gedi_beams = ["BEAM0000", "BEAM0001", "BEAM0010", "BEAM0011", "BEAM0101", "BEAM0110", "BEAM1000", "BEAM1011"]

out_lut = dict()
for tile_name in tqdm.tqdm(tile_names):
    out_lut[tile_name] = list()

orbit_lut_files = glob.glob("/scratch/a.hek4/gedi_files_2021_12_16/data/gedi_orbits_tiled/*.json")
for orbit_lut_file in tqdm.tqdm(orbit_lut_files):
    orbit_lut = rsgislib.tools.utils.read_json_to_dict(orbit_lut_file)

    orbit_vec_file = orbit_lut["file"]

    for beam in gedi_beams:
        beam_tile_names = orbit_lut["beams"][beam]
        for tile_name in beam_tile_names:
            if orbit_vec_file not in out_lut[tile_name]:
                out_lut[tile_name].append(orbit_vec_file)


out_dir = "/scratch/a.hek4/gedi_files_2021_12_16/data/tile_luts"

for tile_name in tqdm.tqdm(tile_names):
    if len(out_lut[tile_name]) > 0:
        rsgislib.tools.utils.write_dict_to_json(out_lut[tile_name], os.path.join(out_dir, f"{tile_name}_lut.json"))


