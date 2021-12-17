from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib.vectorutils
import rsgislib.zonalstats

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        # Create a copy of the input data so analysis doesn't corrupt the input file
        shutil.copy(self.params['gedi_vec_file'], self.params['out_vec_file'])

        # Perform zonal stats and updating the output file with the new column.
        gedi_vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(self.params['gedi_vec_file'])
        for gedi_lyr in gedi_vec_lyrs:
            rsgislib.zonalstats.ext_point_band_values_file(self.params['out_vec_file'], gedi_lyr,
                                                           self.params['input_img'], int(self.params['img_band']),
                                                           float(self.params['min_thres']), float(self.params['max_thres']),
                                                           float(self.params['out_no_data_val']), self.params['out_field'],
                                                           reproj_vec=False, vec_def_epsg=None)


    def required_fields(self, **kwargs):
        return ["tile_name", "gedi_vec_file", "input_img", "img_band", "min_thres",
                "max_thres", "out_no_data_val", "out_field", "out_vec_file"]


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
