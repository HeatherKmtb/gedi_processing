from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import tqdm
import geopandas

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        gpdf = geopandas.read_file(kwargs['vec_file'], layer=kwargs['vec_lyr'])

        for i in tqdm.tqdm(range(gpdf.shape[0])):
            tile_name = gpdf.loc[i]['tile_names']
            out_img = os.path.join(kwargs['out_dir'], '{}.tif'.format(tile_name))

            x_min_val = gpdf.loc[i]['xmin']
            x_max_val = gpdf.loc[i]['xmax']
            y_min_val = gpdf.loc[i]['ymin']
            y_max_val = gpdf.loc[i]['ymax']

            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict['xmin'] = x_min_val
                c_dict['xmax'] = x_max_val
                c_dict['ymin'] = y_min_val
                c_dict['ymax'] = y_max_val
                c_dict['out_img'] = out_img
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(vec_file='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm_overlap_tiles.gpkg',
                              vec_lyr='srtm_tiles',
                              out_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/base_overlap_tiles')

        self.gen_command_info(vec_file='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm_tiles.gpkg',
                              vec_lyr='srtm_tiles',
                              out_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/base_tiles')


        self.pop_params_db()
        self.create_slurm_sub_sh("prep_srtm_tiles", 16448, '/scratch/a.hek4/gedi_files_2021_12_16/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file="db_info_run_file.txt", n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n')

if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'do_tile_analysis'
    process_tools_cls = 'DoTileAnalysis'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.hek4/pbpt_db_info.txt",
                           lock_file_path="/scratch/a.hek4/gedi_files_2021_12_16/tmp/gedi_lock_file.txt",
                           process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()