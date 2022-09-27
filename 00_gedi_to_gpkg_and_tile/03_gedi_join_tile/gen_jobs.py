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
            tiles_vec_file='/bigdata/heather_gedi/git/gedi_processing/glb_land_roi_deg_tiles_named.geojson',
            tiles_vec_lyr='glb_land_roi_deg_tiles_named',
            gedi_tiles='/bigdata/heather_gedi/2.gpkg/GEDI02_B_2019_Q4/*.gpkg',
            out_dir='/bigdata/heather_gedi/data/3.gedi_orbits_tiled')


        self.pop_params_db()
        #self.create_slurm_sub_sh("tile_join_gedi_data", 16448, '/bigdata/heather_gedi/logs',
        #                         run_script='run_exe_analysis.sh',
        #                         db_info_file=None, account_name='scw1403', n_cores_per_job=5, n_jobs=5,
        #                         job_time_limit='2-23:59',
        #                         module_load='module load parallel singularity\n')
        self.create_shell_exe(run_script="run_exe_analysis.sh", cmds_sh_file="cmds_lst.sh", n_cores=25, db_info_file="pbpt_db_info_lcl_file.txt")

if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /bigdata:/bigdata --bind /home/heather:/home/heather /bigdata/heather_gedi/sw_image/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'do_tile_analysis'
    process_tools_cls = 'DoTileAnalysis'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/bigdata/heather_gedi/pbpt_db_info.txt",
                                         lock_file_path="./gedi_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
