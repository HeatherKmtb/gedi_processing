from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import glob
import geopandas
import numpy
import from rasterstats import zonal_stats

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imagecalc.buffer_img_pxl_vals(self.params['gmw_file'], self.params['buffered_gmw'],[1],
                    -1 , self.params['temp_dir'], 'TIF', 1, False)

        gedi_beams = ["BEAM0000", "BEAM0001", "BEAM0010", "BEAM0011", "BEAM0101", "BEAM0110", "BEAM1000", "BEAM1011"]

        for gedi_beam in gedi_beams:
            print(gedi_beam)
            #now add in here rsgislib join function
            vector = geopandas.read_file(self.params['gedi_file'], layer = gedi_beam)
            raster = self.params['buffered_gmw']
            geostats = geopandas.GeoDataFrame.from_features(result)
    
            geostats.to_file(self.params['out_vec_file'], layer = beam, driver='GPKG')


    def required_fields(self, **kwargs):
        return ["tile_name", "gedi_file", "gmw_files", "out_dir", "gmw_dir", "temp_dir"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_vec_file']] = {'type':'gdal_vector', 'chk_proj':True, 'epsg_code':4326}
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_vec_file']):
            os.remove(self.params['out_vec_file'])

if __name__ == "__main__":
    DoTileAnalysis().std_run()
