#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 14:13:39 2022

@author: heatherkay
"""

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

        gmw_tile_file = kwargs['gmw_tile_file']
        gmw_tiles = rsgislib.vectorattrs.read_vec_column(gmw_tile_file, 'gmw_v3_tiles', 'tile')
        
        for tile in gmw_tiles:
            tile_name = self.get_file_basename(tile)
            gedi_file = os.path.join(kwargs['gedi_files'], f'gedi_{tile_name}.gpkg')  
            gmw_file = os.path.join(kwargs['gmw_files'], f'GMW_{tile_name}_2020_v3.gpkg')
            out_vec_file = os.path.join(kwargs['out_dir'], f'gedi_{tile_name}_tiled.gpkg')
            #out_lut_file = os.path.join(kwargs['out_dir'], f'{basename}_lut.json')
            
 #here needs kwargs if filepath is in run_gen_commands but not gen_command_info           
            if (not os.path.exists(out_vec_file)):
                c_dict = dict()
                #c_dict['gmw_tile'] = tile
                c_dict['gedi_file'] = gedi_file
                c_dict['gmw_file'] = gmw_file
                c_dict['out_vec_file'] = out_vec_file
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            gmw_tile_file='/scratch/a.hek4/layers/gmw/gmw_v3_tiles.geojson',
            gmw_files='/scratch/a.hek4/layers/gmw/gmw_v3_2020_raster/',
            gedi_files='/scratch/a.hek4/data/5.gedi_base_tiles/GEDI02_B_2019_Q1/*.gpkg',
            out_dir='/scratch/a.hek4/data/gmw/1.buffered/GEDI02_B_2019_Q1')


        self.pop_params_db()
        self.create_slurm_sub_sh("tile_join_gedi_data", 16448, '/bigdata/heather_gedi/logs',
                                 run_script='run_exe_analysis.sh',
                                 db_info_file=None, account_name='scw1403', n_cores_per_job=5, n_jobs=5,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n')
        #self.create_shell_exe(run_script="run_exe_analysis.sh", cmds_sh_file="cmds_lst.sh", n_cores=25, db_info_file="pbpt_db_info_lcl_file.txt")

if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/rsgislib-dev.sif python {}".format(py_script)

    process_tools_mod = 'do_tile_analysis'
    process_tools_cls = 'DoTileAnalysis'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.hek4/pbpt_db_info.txt",
                           lock_file_path="/scratch/a.hek4/tmp/gedi_lock_file.txt",
                           process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
