from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import attempt_at_l2a

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        
        attempt_at_l2a.gedi02_b_beams_gpkg(self.params["gedifile"], self.params["outfile"], valid_only=False, out_epsg_code=4326)
        



    def required_fields(self, **kwargs):
        return ["gedifile","outfile"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
