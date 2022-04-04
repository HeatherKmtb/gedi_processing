from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pathlib
import shutil
import rsgislib.imageutils
import rsgislib.imagecalc

logger = logging.getLogger(__name__)


class DoTileAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="do_tile_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params["tmp_dir"]):
            os.mkdir(self.params["tmp_dir"])

        rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()

        print("Creating SRTM tile")
        rsgislib.imageutils.resample_img_to_match(
            self.params["base_img"],
            self.params["srtm_img"],
            self.params["out_img"],
            "GTIFF",
            rsgislib.INTERP_CUBICSPLINE,
            datatype=rsgislib.TYPE_16INT,
            no_data_val=-32768,
            multicore=False,
        )

        print("Check if there is valid data within the SRTM tile")
        band_defns = [rsgislib.imagecalc.BandDefn("srtm", self.params["out_img"], 1)]
        prop_vld = rsgislib.imagecalc.calc_prop_true_exp(
            "(srtm>-500)&&(srtm<9000)?1:0", band_defns
        )

        # tmp_valid_data_img = os.path.join(self.params['tmp_dir'], "{}_vld_data.tif".format(self.params['basename']))
        # rsgislib.imagecalc.bandMath(tmp_valid_data_img, '(srtm>-500)&&(srtm<9000)?1:0', 'GTIFF', rsgislib.TYPE_8UINT, band_defns)
        # vld_count = rsgislib.imagecalc.countPxlsOfVal(tmp_valid_data_img, vals=[1])

        if prop_vld > 0:
            print("There is valid data - calc stats")
            rsgislib.imageutils.pop_img_stats(
                self.params["out_img"],
                use_no_data=True,
                no_data_val=-32768,
                calc_pyramids=True,
            )
        else:
            print("There is not any valid data - remove image")
            rsgislib.imageutils.delete_gdal_layer(self.params["out_img"])

        print("Finished")
        pathlib.Path(self.params["out_cmp_file"]).touch()

        if os.path.exists(self.params["tmp_dir"]):
            shutil.rmtree(self.params["tmp_dir"])

    def required_fields(self, **kwargs):
        return [
            "basename",
            "base_img",
            "srtm_img",
            "out_img",
            "out_cmp_file",
            "tmp_dir",
        ]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        if os.path.exists(self.params["out_img"]) and os.path.exists(self.params["out_cmp_file"]):
            files_dict[self.params["out_img"]] = {
                "type": "gdal_image",
                "chk_proj": True,
                "epsg_code": 4326,
            }
        files_dict[self.params["out_cmp_file"]] = "file"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params["out_img"]):
            os.remove(self.params["out_img"])

        if os.path.exists(self.params["out_cmp_file"]):
            os.remove(self.params["out_cmp_file"])


if __name__ == "__main__":
    DoTileAnalysis().std_run()
