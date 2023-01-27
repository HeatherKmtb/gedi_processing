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
import os

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_file = self.params["gedi_file"]
        slope_lut = self.params["slope_lut"]
        temp_dir = self.params["temp_dir"]
        
        os.mkdir(temp_dir)
        
        beams = vectorutils.get_vec_lyrs_lst(gedi_file)
        bbox = vectorutils.get_vec_layer_extent(gedi_file, vec_lyr = beams[0], 
                                                compute_if_exp = True)         
        #small_bbox = geometrytools.buffer_bbox(bbox = bbox, buf = -0.5)
        
        #raster_list = imagelut.query_img_lut(scn_bbox = small_bbox, lut_db_file = slope_lut, 
                                       # lyr_name = 'slope') 
        
    
        #if len(raster_list)>1:
         #   raise Exception('multiple tiles returned' + gedi_file)
        #raster = raster_list[0]
        raster = imagelut.get_raster_lyr(bbox, lut_db_file = slope_lut, lyr_name = 'slope', tmp_dir = temp_dir)
        
        
        for beam in beams:
            
            rsgislib.zonalstats.ext_point_band_values_file(vec_file=gedi_file, 
                        vec_lyr=beam, input_img = raster, img_band= 1, min_thres = 0, 
                        max_thres = 90, out_no_data_val= -99, out_field= 'slope', 
                        reproj_vec = True, vec_def_epsg = None)
            
    

    def required_fields(self, **kwargs):
        return ["gedi_file","slope_lut"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
