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

        gedi_vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(self.params['gedi_vec_file'])
        for gedi_lyr in gedi_vec_lyrs:
            rsgislib.vectorutils.perform_spatial_join(self.params['gedi_vec_file'], gedi_lyr, self.params['join_vec_file'],
                                                      self.params['join_vec_lyr'], self.params['out_vec_file'], gedi_lyr,
                                                      out_format='GPKG', join_how='inner', join_op='within')


    def required_fields(self, **kwargs):
        return ["tile_name", "gedi_vec_file", "join_vec_file", "join_vec_lyr", "out_vec_file"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_vec_file']] = {'type':'gdal_vector', 'chk_proj':True, 'epsg_code':4326}
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_vec_file']):
            os.remove(self.params['out_vec_file'])

if __name__ == "__main__":
    DoTileAnalysis().std_run()
