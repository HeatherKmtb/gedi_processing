from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib.imageutils
import rsgislib.tools.projection

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()
        wkt_str = rsgislib.tools.projection.get_wkt_from_epsg_code(4326)
        pxl_res = 0.000277777777778
        width = int((self.params['xmax'] - self.params['xmin']) / pxl_res)
        height = int((self.params['ymax'] - self.params['ymin']) / pxl_res)
        rsgislib.imageutils.create_blank_img(
            self.params['out_img'], 1, width, height,
            self.params['xmin'],
            self.params['ymax'], pxl_res, (pxl_res * -1), 0, "", wkt_str, 'GTIFF', rsgislib.TYPE_8UINT)
        rsgislib.imageutils.pop_img_stats(self.params['out_img'], False, 0, False)


    def required_fields(self, **kwargs):
        return ["xmin", "xmax", "ymin", "ymax", "out_img"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = {'type':'gdal_image', 'chk_proj':True, 'epsg_code':4326}
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

if __name__ == "__main__":
    DoTileAnalysis().std_run()
