#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:13:39 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas



logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params["gedi_file"]
        out_file = self.params["out_file"]
        wwf = self.params["wwf"]
                       
        beams = ['BEAM0101','BEAM0110','BEAM1000','BEAM1011']
        #stats = 'median'
        for beam in beams:

            base_gdf = geopandas.read_file(file, layer = beam)
            join_gdf = geopandas.read_file(wwf)
           
            geostats = geopandas.sjoin(base_gdf, join_gdf, how='inner', op='within',lsuffix='lefty',rsuffix='righty')
    
            geostats.to_file(out_file, driver='GPKG', crs='EPSG:4326')



    def required_fields(self, **kwargs):
        return ["gedi_file","out_file","wwf"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
