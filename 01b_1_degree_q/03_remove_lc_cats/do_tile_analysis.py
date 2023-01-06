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
from rsgislib import vectorutils

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params["gedi_file"]
        out_file = self.params["out_file"]
                       
        beams = vectorutils.get_vec_lyrs_lst(file)
        cat = [60.0, 50.0, 70.0, 80.0, 200.0, 40.0, 0.0, 100.0, 90.0, 30.0, 20.0]
        column = 'median'

        for beam in beams:
            df = geopandas.read_file(file, layer=beam)
            df2 = df[np.logical_not(df[column].isin(cat))]
            new = df2[df2['landsat_treecover']>10]
            if new.empty:
                continue
            new.to_file(out_file, layer = beam, driver='GPKG')


    def required_fields(self, **kwargs):
        return ["gedi_file","out_file"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
