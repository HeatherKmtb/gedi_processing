#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:10:09 2022

@author: heatherkay
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 13:52:32 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import glob
import rsgislib
import rsgislib.vectorattrs
import os

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        gedi_files = glob.glob(kwargs['gedi_tiles'])

        for gedi_file in gedi_files:
            basename = self.get_file_basename(gedi_file)
            out_file = os.path.join(kwargs['out_dir'], f'{basename}.gpkg')

            if (not os.path.exists(out_file)):
                c_dict = dict()
                c_dict['gedi_file'] = gedi_file
                c_dict['out_file'] = out_file
                c_dict['raster'] = '/bigdata/heather_gedi/layers/PROBAV_LC100_global_v3.0.1_2019-nrt_Discrete-Classification-map_EPSG-4326.tif'
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            gedi_tiles='/bigdata/heather_gedi/data/1_deg_q/1.filter_for_quality/GEDI02_B_2021_Q1/*.gpkg',
            out_dir='/bigdata/heather_gedi/data/1_deg_q/2.join_lc/GEDI02_B_2021_Q1')

        self.pop_params_db()

        self.create_shell_exe(run_script="run_exe_analysis.sh", cmds_sh_file="cmds_lst.sh", n_cores=25, db_info_file="pbpt_db_info_lcl_file.txt")

if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /bigdata:/bigdata --bind /home/heather:/home/heather /bigdata/heather_gedi/sw_image/au-eoed-dev.sif python {}".format(py_script)
    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/bigdata/heather_gedi/pbpt_db_info.txt",lock_file_path="./_lockfile.txt")
    create_tools.parse_cmds()
