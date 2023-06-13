#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:46:52 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas 
from rasterstats import zonal_stats
import numpy as np

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params['gedi_file']
        basename = self.params['basename']
        out_dir = self.params['out_dir']
        
        colNms=['i_h100','i_cd','doy','i_wflen','i_acqdate','b1','vcf','ECO_NAME_lefty','ECO_ID_lefty','BIOME_lefty','geometry']               
        
        gdf = geopandas.read_file(file)
        gdf2 = gdf.astype({'ECO_ID_lefty':'int32'})
        ecoNames = list(np.unique(gdf2['ECO_ID_lefty']))#get list of unique ecoregions    
        
        for eco in ecoNames:
            #create new df with just columns I want
            gdf3 = geopandas.GeoDataFrame(gdf2, columns=colNms)
            ID = str(eco)
            df_eco = gdf2.loc[gdf3['ECO_ID_lefty']==eco, colNms]
            df_eco.to_file(out_dir + '/{}_eco_{}.gpkg'.format(basename, ID), driver='GPKG', crs='EPSG:4326')    


    def required_fields(self, **kwargs):
        return ["gedi_file", "out_dir", "basename"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()
