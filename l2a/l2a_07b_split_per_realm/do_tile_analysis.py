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
from pathlib import Path

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params["gedi_file"]
        out_dir = self.params["out_dir"]
        temp_file = self.params["temp_file"]
                       
        beams = vectorutils.get_vec_lyrs_lst(file)

        for beam in beams:
            basename = os.path.splitext(os.path.basename(file))[0]
            df = geopandas.read_file(file, layer=beam)
            new = df.astype({'REALM':'str'})
            realms = list(np.unique(df['REALM']))

            for realm in realms:
               df_realm = new.loc[new['REALM']==realm] 
               df_realm.to_file(out_dir + '/{}_realm_{}.gpkg'.format(basename,realm), layer = beam, driver='GPKG')

        Path(temp_file)

    def required_fields(self, **kwargs):
        return ["gedi_file","out_dir","temp_file"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
