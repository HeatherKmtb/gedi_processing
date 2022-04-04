from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        base_tiles = glob.glob(kwargs["tiles_srch"])

        for tile_img in base_tiles:
            basename = self.get_file_basename(tile_img)
            basename_sub = basename.replace(kwargs["rm_name_str"], "")
            out_img = os.path.join(kwargs['out_dir'], '{}.kea'.format(basename))
            base_img = os.path.join(kwargs['base_tiles_dir'], '{}.tif'.format(basename_sub))
            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict['basename'] = basename
                c_dict['base_img'] = base_img
                c_dict['tile_img'] = tile_img
                c_dict['out_img'] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        self.gen_command_info(
            tiles_srch='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_aspect_overlap_tiles/*.tif',
            rm_name_str="_aspect",
            base_tiles_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/base_tiles',
            out_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_aspect_tiles')

        self.gen_command_info(
            tiles_srch='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_slope_overlap_tiles/*.tif',
            rm_name_str="_slope",
            base_tiles_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/base_tiles',
            out_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_slope_tiles')

        self.pop_params_db()
        self.create_slurm_sub_sh(
            "cutout_fnl_lyrs",
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
