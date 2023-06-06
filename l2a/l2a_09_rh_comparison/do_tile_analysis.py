#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:13:39 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os.path
import geopandas as gpd
import pandas
import matplotlib.pyplot as plt
from statistics import mean, stdev
from math import sqrt
from scipy import stats as st
import numpy as np
from scipy.stats import gaussian_kde


logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_file = self.params["gedi_file"]
        out_dir = self.params["out_dir"]
        
         
        df1 = gpd.read_file(gedi_file, layer = 'BEAM0101')
        df2 = gpd.read_file(gedi_file, layer = 'BEAM0110')
        df3 = gpd.read_file(gedi_file, layer = 'BEAM1000')
        df4 = gpd.read_file(gedi_file, layer = 'BEAM1011')

        dfList = [df1, df2, df3, df4]

        df = pandas.concat(dfList) 

        df_quality = df[df.quality_flag != 0]

        rh98 = df_quality['rh_98']
        rh100 = df_quality['rh_100']
        
        hd, tl = os.path.split(gedi_file)
        shp_lyr_name = os.path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        biome = name_comp[0] 
        realm = name_comp[1]
        
        #density plot
        xy = np.vstack([rh98,rh100])
        z = gaussian_kde(xy)(xy)

        fig, ax = plt.subplots()
        ax.scatter(rh98, rh100, c=z, s=10)
        plt.rcParams.update({'font.size':12}) 

        ax.set_title('RH98 v RH100')
        ax.set_ylabel('RH100 (m)')
        ax.set_xlabel('RH98 (m)')
        #ax.set_xlim([0, 60])
        #ax.set_ylim([0,1])
        plt.savefig(out_dir + '{}_{}_scatter.png'.format(biome, realm))
        plt.close 



        #boxplot
        box_df = df_quality[['rh_98','rh_100']]
        plt.boxplot(box_df)
        plt.xticks([1,2], ['RH98','RH100'])
        plt.savefig(out_dir + '{}_{}_box.png'.format(biome, realm))

        #boxplots per height range
        fig = plt.figure()
        box5df= box_df[box_df['rh_98']>=5]
        box5to10df = box5df[box5df['rh_98']<=10]
        plt.boxplot(box5to10df)
        plt.xticks([1,2], ['RH98','RH100'])
        plt.title('Height range 5-10m in' + biome + ' ' + realm)
        plt.savefig(out_dir + '{}_{}_test_rh_box_5-10.png'.format(biome, realm))
        plt.close

        fig = plt.figure()
        box10df= box_df[box_df['rh_98']>=10]
        box10to15df = box10df[box10df['rh_98']<=15]
        plt.boxplot(box10to15df)
        plt.xticks([1,2], ['RH98','RH100'])
        plt.title('Height range 10-15m in' + biome + ' ' + realm)
        plt.savefig(out_dir + '{}_{}_test_rh_box_10-15.png'.format(biome, realm))
        plt.close

        fig = plt.figure()
        box15df= box_df[box_df['rh_98']>=15]
        box15to20df = box15df[box15df['rh_98']<=20]
        plt.boxplot(box15to20df)
        plt.xticks([1,2], ['RH98','RH100'])
        plt.title('Height range 15-20m in' + biome + ' ' + realm)
        plt.savefig(out_dir + '{}_{}_test_rh_box_15-20.png'.format(biome, realm))
        plt.close

        fig = plt.figure()
        box20df= box_df[box_df['rh_98']>=20]
        box20to30df = box20df[box20df['rh_98']<=30]
        plt.boxplot(box20to30df)
        plt.xticks([1,2], ['RH98','RH100'])
        plt.title('Height range 20-30m in' + biome + ' ' + realm)
        plt.savefig(out_dir + '{}_{}_test_rh_box_20-30.png'.format(biome, realm))
        plt.close

        fig = plt.figure()
        box30df= box_df[box_df['rh_98']>=30]
        box30to40df = box30df[box30df['rh_98']<=40]
        plt.boxplot(box30to40df)
        plt.xticks([1,2], ['RH98','RH100'])
        plt.title('Height range 30-40m in' + biome + ' ' + realm)
        plt.savefig(out_dir + '{}_{}_test_rh_box_30-40.png'.format(biome, realm))
        plt.close

        fig = plt.figure()
        box5df= box_df[box_df['rh_98']<=5]
        plt.boxplot(box5df)
        plt.xticks([1,2], ['RH98','RH100'])
        plt.title('Height range <5m in' + biome + ' ' + realm)
        plt.savefig(out_dir + '{}_{}_test_rh_box_under_5.png'.format(biome, realm))
        plt.close

        fig = plt.figure()
        box40df= box_df[box_df['rh_98']>=40]
        plt.boxplot(box40df)
        plt.xticks([1,2], ['RH98','RH100'])
        plt.title('Height range >40m in' + biome + ' ' + realm)
        plt.savefig(out_dir + '{}_{}_test_rh_box_over_40.png'.format(biome, realm))
        plt.close

        #t test (unpaired)
        ttest = st.ttest_ind(a=rh98, b=rh100, equal_var=True)

        #cohens d
        cohens_d = (mean(rh100) - mean(rh98)) / (sqrt((stdev(rh100) ** 2 + stdev(rh98) ** 2) / 2))

        #pearsons r
        pearson = st.pearsonr(rh100,rh98)
    
        results = pandas.DataFrame(columns = ['biome', 'realm', 'ttest', 'cohens', 'pearson'])
        res = pandas.Series([biome, realm, ttest, cohens_d, pearson], index = ['biome', 'realm', 'ttest', 'cohens', 'pearson'])
        results = pandas.concat([results, res.to_frame().T], ignore_index=True)

        results.to_csv(out_dir + '{}_{}.csv'.format(biome, realm))        


    def required_fields(self, **kwargs):
        return ["gedi_files","out_file"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()
