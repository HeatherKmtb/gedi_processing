from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import glob
import geopandas
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_files = glob.glob(self.params['gedi_tiles'])

        tile_gpdf = geopandas.read_file(self.params['tiles_vec_file'], layer=self.params['tiles_vec_lyr'])
        print(tile_gpdf)
        tile_gpdf = tile_gpdf[tile_gpdf["tile_name"]==self.params['tile_name']]
        print(tile_gpdf)
        #vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(gedi_files[0])


    def required_fields(self, **kwargs):
        return ["tiles_vec_file", "tiles_vec_lyr", "tile_name", "gedi_tiles", "out_file"]


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
