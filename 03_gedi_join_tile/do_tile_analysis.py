from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(self.params['gedi_file'])
        for gedi_lyr in gedi_vec_lyrs:
            rsgislib.vectorutils.perform_spatial_join(self.params['gedi_file'], gedi_lyr, self.params['tiles_vec_file'],
                                                      self.params['tiles_vec_lyr'], self.params['out_file'], gedi_lyr,
                                                      out_format='GPKG', join_how='inner', join_op='within')


    def required_fields(self, **kwargs):
        return ["tiles_vec_file", "tiles_vec_lyr", "gedi_file", "out_file"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_file']] = 'gdal_vector'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

if __name__ == "__main__":
    DoTileAnalysis().std_run()
