#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:31:27 2024

@author: alex
"""



import os

import multiprocessing
import numpy as np
import pandas as pd

import os

#import multiprocessing
import numpy as np
import pandas as pd
import shutil
import sys

import os , glob
import sys, subprocess
import itertools

master_sheet_path = '/Users/alex/brain_data/AD_DECODE/AD_DECODE_data.xlsx'
master_excel = pd.ExcelFile(master_sheet_path)
master = pd.read_excel(master_excel)
column_master=master['MRI_Exam']
column_master2 = ["S0"+str(s) for s in  column_master] 
column_master2 = [str(s).replace(" ","") for s in column_master2]
column_master2[79] = 'S00775'
common_path = '/Users/alex/brain_data/AD_DECODE/common_runnos.csv'
common_df = pd.read_csv(common_path) #, header=None)
column_to_compare = common_df['MRI_Exam']
column_to_compare = [str(s).replace(" ","") for s in column_to_compare]


# Find the intersection between the column and the list
intersection = np.intersect1d(column_to_compare, column_master2)

indices_array1 = np.isin(column_master2,column_to_compare)
master_short = master.iloc[indices_array1,:]

master_short.to_excel('/Users/alex/brain_data/AD_DECODE/AD_DECODE_data_short.xlsx', index=False)
#indices_array1 = np.where(np.isin(common_excel.iloc[:, 0][0],S_master.iloc[:, 0]))

