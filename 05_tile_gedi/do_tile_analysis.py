from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import glob
import geopandas
import numpy
import rsgislib.vectorutils
import rsgislib.tools.utils

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_files = rsgislib.tools.utils.read_json_to_dict(self.params['tile_lut_file'])

        #tile_gpdf = geopandas.read_file(self.params['tiles_vec_file'], layer=self.params['tiles_vec_lyr'])
        #tile_gpdf = tile_gpdf[tile_gpdf["tile_name"]==self.params['tile_name']]
        #print(tile_gpdf)

        gedi_beams = ["BEAM0000", "BEAM0001", "BEAM0010", "BEAM0011", "BEAM0101", "BEAM0110", "BEAM1000", "BEAM1011"]

        for gedi_beam in gedi_beams:
            for gedi_vec_file in gedi_files:
                print(gedi_vec_file)
                gedi_vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(gedi_vec_file)
                first = True
                if gedi_beam in gedi_vec_lyrs:
                    gedi_df = geopandas.read_file(gedi_vec_file, layer=gedi_beam)
                    gedi_df = gedi_df[gedi_df["tile_name"] == self.params['tile_name']]
                    if not gedi_df.empty:
                        print("Not Empty")
                        print(gedi_df.shape)
                    else:
                        print("Empty")
                    """
                    gedi_df["msk_rsgis_sel"] = numpy.zeros((gedi_df.shape[0]), dtype=bool)
                    inter = gedi_df["geometry"].intersects(tile_gpdf.iloc[0]["geometry"])
                    gedi_df.loc[inter, "msk_rsgis_sel"] = True
                    gedi_df = gedi_df[gedi_df["msk_rsgis_sel"]]
                    gedi_df = gedi_df.drop(["msk_rsgis_sel"], axis=1)
                    if not gedi_df.empty:
                        print("Not Empty")
                    else:
                        print("Empty")
                    
                    if first:
                        
                        first = False
                    else:
                    """


    def required_fields(self, **kwargs):
        return ["tile_name", "tile_lut_file", "out_file"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_file']] = {'type':'gdal_vector', 'chk_proj':True, 'epsg_code':4326}
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

if __name__ == "__main__":
    DoTileAnalysis().std_run()
