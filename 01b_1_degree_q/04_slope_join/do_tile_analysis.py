#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:13:39 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas
from rasterstats import zonal_stats
from rsgislib import vectorutils

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params["gedi_file"]
        out_file = self.params["out_file"]
        raster = self.params["raster"]
                       
        beams = vectorutils.get_vec_lyrs_lst(file)
        stats = 'median'

        for beam in beams:
            vector = geopandas.read_file(file, layer=beam)
            result = zonal_stats(vector, raster, stats=stats, geojson_out=True)
            geostats = geopandas.GeoDataFrame.from_features(result, crs='EPSG:4326')
            geostats.to_file(out_file, layer = beam, driver='GPKG')


    def required_fields(self, **kwargs):
        return ["gedi_file","out_file","raster"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
