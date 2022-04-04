from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib.imageutils
import rsgislib.imagecalc
import rsgislib.elevation

logger = logging.getLogger(__name__)


class DoTileAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="do_tile_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params["tmp_dir"]):
            os.mkdir(self.params["tmp_dir"])

        rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()

        pxl_size_img = os.path.join(self.params["tmp_dir"], "{}_pxl_size.kea".format(self.params["basename"]))
        rsgislib.imageutils.calc_wsg84_pixel_size(self.params["srtm_img"], output_img=pxl_size_img, gdalformat='KEA')

        rsgislib.elevation.slope_pxl_res_img(self.params["srtm_img"], pxl_size_img, self.params["out_slope_img"], "GTIFF", unit="degrees")
        rsgislib.imageutils.pop_img_stats(self.params["out_slope_img"], use_no_data=False, no_data_val=0, calc_pyramids=True)

        rsgislib.elevation.aspect_pxl_res_img(self.params["srtm_img"], pxl_size_img, self.params["out_aspect_img"], "GTIFF")
        rsgislib.imageutils.pop_img_stats(self.params["out_aspect_img"], use_no_data=False, no_data_val=0, calc_pyramids=True)

        if os.path.exists(self.params["tmp_dir"]):
            shutil.rmtree(self.params["tmp_dir"])

    def required_fields(self, **kwargs):
        return [
            "basename",
            "srtm_img",
            "out_slope_img",
            "out_aspect_img",
            "tmp_dir",
        ]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_slope_img"]] = {
            "type": "gdal_image",
            "chk_proj": True,
            "epsg_code": 4326,
        }
        files_dict[self.params["out_aspect_img"]] = {
            "type":      "gdal_image",
            "chk_proj":  True,
            "epsg_code": 4326,
            }
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params["out_slope_img"]):
            os.remove(self.params["out_slope_img"])

        if os.path.exists(self.params["out_aspect_img"]):
            os.remove(self.params["out_aspect_img"])


if __name__ == "__main__":
    DoTileAnalysis().std_run()
