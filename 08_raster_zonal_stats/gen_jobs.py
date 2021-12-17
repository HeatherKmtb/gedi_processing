from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib
import rsgislib.vectorattrs

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_gedi_dir']):
            os.mkdir(kwargs['out_gedi_dir'])

        tile_names = rsgislib.vectorattrs.read_vec_column(kwargs['tiles_vec_file'], kwargs['tiles_vec_lyr'], att_column='tile_name')

        for tile_name in tile_names:
            in_vec_file = os.path.join(kwargs['in_gedi_dir'], f'{tile_name}.gpkg')
            out_vec_file = os.path.join(kwargs['out_gedi_dir'], f'{tile_name}.gpkg')

            if (not os.path.exists(out_vec_file)) and os.path.exists(in_vec_file):
                c_dict = dict()
                c_dict['tile_name'] = tile_name
                c_dict['gedi_vec_file'] = in_vec_file
                c_dict['input_img'] = kwargs['input_img']
                c_dict['img_band'] = kwargs['img_band']
                c_dict['min_thres'] = kwargs['min_thres']
                c_dict['max_thres'] = kwargs['max_thres']
                c_dict['out_no_data_val'] = kwargs['out_no_data_val']
                c_dict['out_field'] = kwargs['out_field']
                c_dict['out_vec_file'] = out_vec_file
                self.params.append(c_dict)


    def run_gen_commands(self):
        # Join the ESA WorldCover
        self.gen_command_info(
            tiles_vec_file='../glb_land_roi_deg_tiles_named.geojson',
            tiles_vec_lyr='glb_land_roi_deg_tiles_named',
            in_gedi_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/gedi_base_tiles',
            input_img='/scratch/a.hek4/esa_worldcover/esa_worldcover.vrt',
            img_band=1,
            min_thres=0,
            max_thres=100,
            out_no_data_val=-1,
            out_field="worldcover",
            out_gedi_dir='/scratch/a.hek4/gedi_files_2021_12_16/data/gedi_tiles_stats_s1')

        # If you want to perform zonal stats to another raster layer then copy the self.gen_command_info call
        # and change the input in_gedi_dir and out_gedi_dir for the appropriate gedi data
        # and then update the input_img and img_band variables for the layer stats are to be calculated.
        # You will also need to define the valid raster data range (min_thres, max_thres) and the output
        # no data value. Finally, define the column name (out_field) to be written to the output vector layer.


        self.pop_params_db()
        self.create_slurm_sub_sh("tile_gedi_data", 16448, '/scratch/a.hek4/gedi_files_2021_12_16/logs',
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