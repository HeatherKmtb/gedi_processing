from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import glob
import geopandas
import numpy
import rsgislib.zonalstats
import rsgislib.imagemorphology

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imagemorphology.create_circular_op(output_file='CircularOp3.gmtxt', op_size=3)

        rsgislib.imagemorphology.image_erode(self.params['gmw_file'], self.params['buffered_gmw'], 
                                             'CircularOp3.gmtxt', True, 3, 'GTiff', rsgislib.TYPE_8UINT)
        gedi_beams = ["BEAM0000", "BEAM0001", "BEAM0010", "BEAM0011", "BEAM0101", "BEAM0110", "BEAM1000", "BEAM1011"]
        #stats='median'
        
        for gedi_beam in gedi_beams:
            print(gedi_beam)
            #now add in here rsgislib join function
            vec_file = geopandas.read_file(self.params['gedi_file'], layer = gedi_beam)
            input_img = self.params['buffered_gmw']
            #result = zonal_stats(vector, raster, stats=stats, geojson_out=True)
            result = rsgislib.zonalstats.ext_point_band_values_file(vec_file, gedi_beam,
                    input_img, '1', '1', '1', '-999', 'gmw', reproj_vec=False, vec_def_epsg=None)
            df = geopandas.GeoDataFrame.from_features(result)
            #query geostats and remove all features with no data value
            cleandf = df[df['gmw']==1]
            if not cleandf.empty:
                cleandf.to_file(self.params['out_vec_file'], layer = gedi_beam, driver='GPKG')
            if cleandf.empty:
                continue


    def required_fields(self, **kwargs):
        return ["gedi_file", "gmw_file", "out_vec_file", "buffered_gmw"]


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
