#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 10:34:45 2023

@author: heatherkay
"""

from os import path
#from scipy.stats import gaussian_kde
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import glob
#import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap
import geopandas

gedifiles = glob.glob('/bigdata/heather_gedi/data/1_deg_q/3.remove_lc_cats/GEDI02_B_2020_Q1/*.gpkg')
out_dir='/bigdata/heather_gedi/results/1_deg/GEDI02_B_2020_Q1'
out_file='/bigdata/heather_gedi/results/1_deg/2020_Q1.csv'
quarter = '2020_Q1'

#create df for results
resultsa = pd.DataFrame(columns = ['Grid', 'qout', 'deg_free', 'mse'])

for file in gedifiles: 
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[1] 
        print(name)
        
        df1 = geopandas.read_file(file, layer='BEAM0101')
        df2 = geopandas.read_file(file, layer='BEAM0110')
        df3 = geopandas.read_file(file, layer='BEAM1000')    
        df4 = geopandas.read_file(file, layer='BEAM1011') 
        
        df = pd.concat([df1,df2,df3,df4])
         
        #calculate canopy density
        rv = df['rv']
        rg = df['rg']
        cd = rv/(rv + rg)
        df['cd'] = cd
        final = df.dropna(subset = ['cd'])

        if final.empty:
            continue
        
        #convert height to metres
        incm = final['rh100']
        x = incm/100
        final['h100']=x 
        
        del x, rv, rg
                
        footprints = len(final['h100'])
        
        if footprints < 100:
            continue
            
        #regression 
        def f(x,q):
            return 1- np.exp(-q * x)
    
        x = final['h100'].to_numpy()
        y = final['cd'].to_numpy() 
        #x = np.append(x, [0])
        #y = np.append(y, [0])
    
        qout, qcov = curve_fit(f, x, y, 0.04)
        qout = qout.round(decimals=4)
        
        y_predict = f(x, qout)
            
        from sklearn.metrics import mean_squared_error

        mse = mean_squared_error(y, y_predict)
        mse = round(mse, 3)        

        resultsa = resultsa.append({'Grid': name, 'qout': qout, 
                                    'deg_free': footprints, 
                                    'mse': mse, 'quarter':quarter}, 
                                    ignore_index=True)

        resultsa.to_csv(out_file)

#alternative plotting with mpl_scatter_density
        # "Viridis-like" colormap with white background
        white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
            (0, '#ffffff'),
            (1e-20, '#440053'),
            (0.2, '#404388'),
            (0.4, '#2a788e'),
            (0.6, '#21a784'),
            (0.8, '#78d151'),
            (1, '#fde624'),
        ], N=256)
        
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
        density = ax.scatter_density(x, y, cmap=white_viridis)
        fig.colorbar(density, label='Number of points per pixel')

        #mpl_scatter_density(fig, x, y)

        ax.set_title('Grid square ' + name)
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
        plt.savefig(out_dir + 'fig{}_{}.pdf'.format(quarter, name))
        plt.close 
        del fig

