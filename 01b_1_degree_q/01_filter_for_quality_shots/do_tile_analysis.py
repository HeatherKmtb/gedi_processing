#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:46:52 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import geopandas as gpd

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params['gedi_file']
        out_file = self.params['out_file']
        
        
        gedi_beams = ["BEAM0101", "BEAM0110", "BEAM1000", "BEAM1011"]
        
        for beam in gedi_beams:
            #print(gedi_lyr)
            df = gpd.read_file(file, layer=beam)
            df2 = df[df['l2a_quality_flag']==1]
            df3 = df2[df2['l2b_quality_flag']==1]
            df4 = df3[df3['solar_elevation']<0]
            if df4.empty:
                continue
            df4.to_file(out_file, layer=beam, driver='GPKG')
        

    def required_fields(self, **kwargs):
        return ["gedi_file", "out_file"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()