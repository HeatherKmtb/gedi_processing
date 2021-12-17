from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import tqdm
import rsgislib.vectorutils
import rsgislib.vectorattrs
import rsgislib.tools.utils

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(self.params['gedi_file'])
        tile_lut = dict()
        tile_lut["file"] = self.params['out_vec_file']
        tile_lut["beams"] = dict()
        for gedi_lyr in tqdm.tqdm(gedi_vec_lyrs):
            #print(gedi_lyr)
            rsgislib.vectorutils.perform_spatial_join(self.params['gedi_file'], gedi_lyr, self.params['tiles_vec_file'],
                                                      self.params['tiles_vec_lyr'], self.params['out_vec_file'], gedi_lyr,
                                                      out_format='GPKG', join_how='inner', join_op='within')

            tile_names = rsgislib.vectorattrs.get_unq_col_values(self.params['out_vec_file'], gedi_lyr, col_name="tile_name")
            tile_names_lst = list()
            for tile_name in tile_names:
                tile_names_lst.append(str(tile_name))
            tile_lut["beams"][gedi_lyr] = tile_names_lst

        rsgislib.tools.utils.write_dict_to_json(tile_lut, self.params['out_lut_file'])



    def required_fields(self, **kwargs):
        return ["tiles_vec_file", "tiles_vec_lyr", "gedi_file", "out_vec_file", "out_lut_file"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_vec_file']] = {'type':'gdal_vector', 'chk_proj':True, 'epsg_code':4326}
        files_dict[self.params['out_lut_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_vec_file']):
            os.remove(self.params['out_vec_file'])

        if os.path.exists(self.params['out_lut_file']):
            os.remove(self.params['out_lut_file'])

if __name__ == "__main__":
    DoTileAnalysis().std_run()
