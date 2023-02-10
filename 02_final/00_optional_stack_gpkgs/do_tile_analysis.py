#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:46:52 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        out_file = self.params['out_file']
        gedi_files = self.params["gedi_files"]
                       
        rsgislib.vectorutils.merge_vectors_to_gpkg_ind_lyrs(gedi_files,
                            out_file, rename_dup_lyrs = True)   


    def required_fields(self, **kwargs):
        return ["gedi_file", "out_file", "raster"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()