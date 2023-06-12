#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:46:52 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas
#from rasterstats import zonal_stats

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params['gedi_file']
        out_file = self.params['out_file']
        wwf = self.params["wwf"]
                       
        
        glas = geopandas.read_file(file)
        base_gdf = glas.to_crs(crs=4326)
        join_gdf = geopandas.read_file(wwf)
           
        geostats = geopandas.sjoin(base_gdf, join_gdf, how='inner', op='within',lsuffix='lefty',rsuffix='righty')
    
        geostats.to_file(out_file, driver='GPKG', crs='EPSG:4326')

    def required_fields(self, **kwargs):
        return ["gedi_file", "out_file", "wwf"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
