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
import os.path
import logging
import glob

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        biomes = ['1','2','3','4','5','6','7','8','9',
                  '10','11','12','13','14']
        
        for biome in biomes:
            gedi_files = glob.glob(kwargs['gedi_dir'] + biome + '/*.gpkg')
            
            
            out_dir = kwargs['out_dir']
        
            for gedi_file in gedi_files:
                basename = self.get_file_basename(gedi_file)
                temp_file = os.path.join(kwargs['temp_dir'], f'{basename}.gpkg')

                if (not os.path.exists(temp_file)):
                    c_dict = dict()
                    c_dict['gedi_file'] = gedi_file
                    c_dict['out_dir'] = out_dir
                    c_dict['temp_file'] = temp_file
                    self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            gedi_dir='/bigdata/heather_gedi/data/l2a/6.split_per_biome/',
            out_dir='/bigdata/heather_gedi/data/l2a/6b.split_per_realm',
            temp_dir='bigdata/heather_gedi/data/l2a/6b.split_per_realm_filenames')

        self.pop_params_db()

        self.create_shell_exe(run_script="run_exe_analysis.sh", cmds_sh_file="cmds_lst.sh", n_cores=25, db_info_file="pbpt_db_info_lcl_file.txt")

if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /bigdata:/bigdata --bind /home/heather:/home/heather /bigdata/heather_gedi/sw_image/au-eoed-dev.sif python {}".format(py_script)
    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/bigdata/heather_gedi/pbpt_db_info.txt",lock_file_path="./_lockfile.txt")
    create_tools.parse_cmds()
