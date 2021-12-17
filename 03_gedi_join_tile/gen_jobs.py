from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib
import rsgislib.vectorattrs

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        gedi_files = glob.glob(kwargs['gedi_tiles'])

        for gedi_file in gedi_files:
            basename = self.get_file_basename(gedi_file)
            out_vec_file = os.path.join(kwargs['out_dir'], f'{basename}_tiled.gpkg')
            out_lut_file = os.path.join(kwargs['out_dir'], f'{basename}_lut.json')

            if (not os.path.exists(out_vec_file)) or (not os.path.exists(out_lut_file)):
                c_dict = dict()
                c_dict['tiles_vec_file'] = kwargs['tiles_vec_file']
                c_dict['tiles_vec_lyr'] = kwargs['tiles_vec_lyr']
                c_dict['gedi_file'] = gedi_file
                c_dict['out_vec_file'] = out_vec_file
                c_dict['out_lut_file'] = out_lut_file
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            tiles_vec_file='../glb_land_roi_deg_tiles_named.geojson',
            tiles_vec_lyr='glb_land_roi_deg_tiles_named',
            gedi_tiles='/scratch/a.hek4/gedi_gpkg_ard/ard/*.gpkg',
            out_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/gedi_orbits_tiled')


        self.pop_params_db()
        self.create_slurm_sub_sh("tile_join_gedi_data", 16448, '/scratch/a.hek4/gedi_files_2021_12_16/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file="db_info_run_file.txt", n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n')

if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/rsgislib-dev.sif python {}".format(py_script)

    process_tools_mod = 'do_tile_analysis'
    process_tools_cls = 'DoTileAnalysis'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.hek4/pbpt_db_info.txt",
                                         lock_file_path="/scratch/a.hek4/gedi_files_2021_12_16/tmp/gedi_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()