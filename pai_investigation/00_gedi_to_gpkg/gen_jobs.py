
from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import os.path
import logging
import glob
import os

logger = logging.getLogger(__name__)

class CreateTestCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        gedifiles = glob.glob('/bigdata/GEDI/GEDI02_A_2020_Q2/*.h5')        
        #print(len(gedifiles))
        for gedifile in gedifiles:
            c_dict = dict()
            c_dict["gedifile"]=gedifile
            name = os.path.splitext(os.path.basename(gedifile))[0]
            c_dict["outfile"]='/bigdata/heather_gedi/data/l2a/1.to_gpkg/' + name + '.gpkg'
            if not os.path.exists(c_dict["outfile"]):
                self.params.append(c_dict)
            
    def run_gen_commands(self):
        self.gen_command_info()
        self.pop_params_db()
        #self.create_slurm_sub_sh("to_gpkg", 8224, '/bigdata/heather_gedi/logs', run_script="exe_analysis.sh",
        #                          db_info_file=None, account_name='scw1403', n_cores_per_job=5, n_jobs=5, job_time_limit='2-23:59',
        #                          module_load='module load parallel singularity\n')
        
        self.create_shell_exe(run_script="run_exe_analysis.sh", cmds_sh_file="cmds_lst.sh", n_cores=25, db_info_file="pbpt_db_info_lcl_file.txt")

    def run_check_outputs(self):
        process_tools_mod = 'perform_processing'
        process_tools_cls = 'ProcessJob'
        time_sample_str = self.generate_readable_timestamp_str()
        out_err_file = 'processing_errs_{}.txt'.format(time_sample_str)
        out_non_comp_file = 'non_complete_errs_{}.txt'.format(time_sample_str)
        self.check_job_outputs(process_tools_mod, process_tools_cls, out_err_file, out_non_comp_file)

    def run_remove_outputs(self, all_jobs=False, error_jobs=False):
        process_tools_mod = 'perform_processing'
        process_tools_cls = 'ProcessJob'
        self.remove_job_outputs(process_tools_mod, process_tools_cls, all_jobs, error_jobs)


if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /bigdata:/bigdata --bind /home/heather:/home/heather /bigdata/heather_gedi/sw_image/au-eoed-dev.sif python {}".format(py_script)
    create_tools = CreateTestCmds(cmd=script_cmd, db_conn_file="/bigdata/heather_gedi/pbpt_db_info.txt",lock_file_path="./_lockfile.txt")
    create_tools.parse_cmds()

