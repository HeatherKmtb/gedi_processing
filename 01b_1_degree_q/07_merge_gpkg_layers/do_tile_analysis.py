#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:13:39 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os.path
import geopandas
import numpy as np
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params["gedi_file"]
        out_file = self.params["out_file"]
        quarter = self.params['quarter']
                       
        rsgislib.vectorutils.merge_vector_lyrs_to_gpkg(vec_file = file,
                out_vec_file = out_file, out_vec_lyr = quarter, 
                exists = False)


    def required_fields(self, **kwargs):
        return ["gedi_file","out_file"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
