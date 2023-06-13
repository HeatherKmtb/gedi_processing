import glob
import pandas as pd

csvs = glob.glob('/bigdata/heather_gedi/results/glas/csvs/*.csv')
out_file = '/bigdata/heather_gedi/results/glas/final_glas.csv'


dfList = [pd.read_csv(c) for c in csvs]
    
df = pd.concat(dfList)  
df.to_csv(out_file)


