#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:13:39 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
from os import path
from scipy.stats import gaussian_kde
import geopandas
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import glob
from rsgislib import vectorutils
from sklearn.metrics import mean_squared_error

#gedifiles = glob.glob('/bigdata/heather_gedi/data/1_deg_q/3.remove_lc_cats/GEDI02_B_2020_Q1/*.gpkg')
#out_dir='/bigdata/heather_gedi/results/1_deg/GEDI02_B_2020_Q1'
#out_file='/bigdata/heather_gedi/results/1_deg/2020_Q1.csv'
#quarter = '2020_Q1'

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params['gedi_file']
        out_fig_dir = self.params['out_fig_dir']
        out_csv_file = self.params['out_csv_file']

        #create df for results
        resultsa = pd.DataFrame(columns = ['Grid', 'eco', 'qout_glas', 'deg_free_glas', 'mse_glas',
                                           'mean_h_glas', 'mean_cd_glas', 'max_h_glas'])


        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[1] 
        eco = name_comp[3]
        print(name)
        print(eco)
        
        layers = vectorutils.get_vec_lyrs_lst(file)
            
        df_list = [geopandas.read_file(file, layer=layer) for layer in layers]
        df = pd.concat(df_list)
         
        #calculate canopy density
        rv = df['rv']
        rg = df['rg']
        cd = rv/(rv + rg)
        df['cd'] = cd
        final = df.dropna(subset = ['cd'])
        
        del rv, rg
                
        footprints = len(final['h100'])
                
        #regression 
        def f(x,q):
           return 1- np.exp(-q * x)
    
        x = final['i_h100'].to_numpy()
        y = final['i_cd'].to_numpy() 

        qout, qcov = curve_fit(f, x, y, 0.04)
        qout = qout.round(decimals=4)
        
        y_predict = f(x, qout)
            
        mse = mean_squared_error(y, y_predict)
        mse = round(mse, 3)        

        meanh = np.mean(x)
        meancd = np.mean(y)
        maxh = np.max(x)
        
        resultsa = resultsa.append({'Grid': name, 'eco':eco, 'qout_glas': qout, 
                                    'deg_free_glas': footprints, 
                                    'mse_glas': mse,
                                    'mean_h_glas': meanh, 'mean_cd_glas': meancd, 
                                    'max_h_glas': maxh}, 
                                    ignore_index=True)

        resultsa.to_csv(out_csv_file)

        xy = np.vstack([x,y])
        z = gaussian_kde(xy)(xy)

        fig, ax = plt.subplots()
        ax.scatter(x, y, c=z, s=10)
        plt.rcParams.update({'font.size':12}) 

        ax.set_title('Ecoregion ' + eco + 'in grid square ' + name)
        ax.set_ylabel('Canopy Density')
        ax.set_xlabel('Height - h100 (m)')
        ax.set_xlim([0, 60])
        ax.set_ylim([0,1])
        #plotting regression
        #putting x data in an order, cause that's what the code needs
        xdata = np.linspace(0, 60)
        #for each value of x calculating the corresponding y value
        ycurve = [f(t, qout) for t in xdata]
        #plotting the curve
        ax.plot(xdata, ycurve, linestyle='-', color='red')
        #adding qout, mse and deg_free to plot
        #ax.annotate('adj_r2 = ' + str(adj_r2[0]), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.15), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('MSE = ' + str(mse), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('No of footprints = ' + str(footprints),xy=(0.975,0.05), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        plt.savefig(out_fig_dir + 'fig{}_{}.png'.format(name, eco))
        plt.close 


    def required_fields(self, **kwargs):
        return ["gedi_file", "out_fig_dir", "out_csv_file"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()