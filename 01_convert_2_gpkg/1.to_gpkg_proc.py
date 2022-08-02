from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import pysl4land.pysl4land_gedi

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        
        pysl4land.pysl4land_gedi.gedi02_b_beams_gpkg(self.params["gedifile"], self.params["outfile"], False, 4326)
        



    def required_fields(self, **kwargs):
        return ["gedifile","outfile"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
