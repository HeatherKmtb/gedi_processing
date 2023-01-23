#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:13:39 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas
from rsgislib import vectorutils
import rsgislib.zonalstats
from rsgislib.imageutils import imagelut
from rsgislib.tools import geometrytools

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_file = self.params["gedi_file"]
        slope_lut = self.params["slope_lut"]
        
        beams = vectorutils.get_vec_lyrs_lst(gedi_file)
        bbox = vectorutils.get_vec_layer_extent(gedi_file, vec_lyr = beams[0], 
                                                compute_if_exp = True)         
        small_bbox = geometrytools.buffer_bbox(bbox = bbox, buf = 0.9)
        
        raster = imagelut.query_img_lut(scn_bbox = small_bbox, lut_db_file = slope_lut, 
                                        lyr_name = 'slope') 
       
        for beam in beams:
            
            rsgislib.zonalstats.ext_point_band_values_file(vec_file=gedi_file, 
                        vec_lyr=beam, input_img = raster, img_band= 1, min_thres = 0, 
                        max_thres = 90, out_no_data_val= -99, out_field= 'slope', 
                        reproj_vec = True, vec_def_epsg = 4326)
            


    def required_fields(self, **kwargs):
        return ["gedi_file","slope_lut"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
