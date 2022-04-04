from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_asp_dir']):
            os.mkdir(kwargs['out_asp_dir'])
        if not os.path.exists(kwargs['out_slp_dir']):
            os.mkdir(kwargs['out_slp_dir'])

        base_tiles = glob.glob(kwargs["tiles_srch"])

        for tile_img in base_tiles:
            basename = self.get_file_basename(tile_img)
            out_slope_img = os.path.join(kwargs['out_slp_dir'], '{}_slope.kea'.format(basename))
            out_aspect_img = os.path.join(kwargs['out_asp_dir'], '{}_aspect.kea'.format(basename))

            if (not os.path.exists(out_slope_img)) or (not os.path.exists(out_aspect_img)):
                c_dict = dict()
                c_dict['basename'] = basename
                c_dict['srtm_img'] = tile_img
                c_dict['out_slope_img'] = out_slope_img
                c_dict['out_aspect_img'] = out_aspect_img
                c_dict["tmp_dir"] = os.path.join(kwargs["tmp_dir"], "{}_gen_tile".format(basename))
                if not os.path.exists(c_dict["tmp_dir"]):
                    os.mkdir(c_dict["tmp_dir"])
                self.params.append(c_dict)

    def run_gen_commands(self):
        self.gen_command_info(
            tiles_srch='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_overlap_tiles/*.kea',
            out_asp_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_aspect_overlap_tiles',
            out_slp_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_slope_overlap_tiles',
            tmp_dir="/scratch/a.hek4/gedi_files_2021_12_16/tmp",
        )

        self.pop_params_db()
        self.create_slurm_sub_sh(
            "pop_srtm_overlap_tiles",
            16448,
            "/scratch/a.hek4/gedi_files_2021_12_16/logs",
            run_script="run_exe_analysis.sh",
            job_dir="job_scripts",
            db_info_file="db_info_run_file.txt",
            n_cores_per_job=10,
            n_jobs=10,
            job_time_limit="2-23:59",
            module_load="module load parallel singularity\n",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif python {}".format(
        py_script
    )

    process_tools_mod = "do_tile_analysis"
    process_tools_cls = "DoTileAnalysis"

    create_tools = GenCmds(
        cmd=script_cmd,
        db_conn_file="/home/a.hek4/pbpt_db_info.txt",
        lock_file_path="/scratch/a.hek4/gedi_files_2021_12_16/tmp/gedi_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )
    create_tools.parse_cmds()
