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

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params["gedi_file"]
        out_file = self.params["out_file"]
                       
        beams = ['BEAM0101','BEAM0110',
                 'BEAM1000','BEAM1011']
        cat = [0.0, 100.0, 90.0, 30.0]
        column = 'median'

        for beam in beams:
            df = geopandas.read_file(file, layer=beam)
            new = df[np.logical_not(df[column].isin(cat))]
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
