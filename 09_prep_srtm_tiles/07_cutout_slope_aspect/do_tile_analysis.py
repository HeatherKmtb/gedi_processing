from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib.imageutils
import rsgislib.imagecalc

logger = logging.getLogger(__name__)


class DoTileAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="do_tile_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('base', self.params["base_img"], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('data', self.params["tile_img"], 1))
        rsgislib.imagecalc.band_math(self.params["out_img"], 'data', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.imageutils.pop_img_stats(self.params["out_img"], use_no_data=False, no_data_val=0, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return [
            "basename",
            "base_img",
            "tile_img",
            "out_img",
        ]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_img"]] = {
            "type": "gdal_image",
            "chk_proj": True,
            "epsg_code": 4326,
        }
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params["out_img"]):
            os.remove(self.params["out_img"])


if __name__ == "__main__":
    DoTileAnalysis().std_run()
