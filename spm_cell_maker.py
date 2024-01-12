#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 13:42:51 2023

@author: ali
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





Factor1 = "genotype" 
Factor2 = "sex"
Factor3 = "Age_cat"
Factor4 = "Treatment"
Factor5 = "HN"
Factor = [Factor1 , Factor2  ]


contrast = 'QSM'

#read the files 
root_path = '/Users/alex/brain_data/AD_DECODE/' +contrast+ '_zscored_u/'
list__files = os.listdir(root_path)
#list__files = [i for i in list__files if 'mrtrixfa' in i]

Current_ID = [i.partition('_'+contrast+'_to_MDT.nii')[0] for i in list__files]
Current_ID = [i for i in Current_ID if "S" in i]
Current_ID = [s.replace('S0', '') for s in Current_ID]




#read master sheet  
master_sheet_path = '/Users/alex/brain_data/AD_DECODE/AD_DECODE_data.xlsx'
master_excel = pd.ExcelFile(master_sheet_path)
master = pd.read_excel(master_excel)
master['genotype'] = master['genotype'].str.strip()
index_23=  master['genotype'] == "APOE23"
master['genotype'][index_23] = "APOE33"
index_34=  master['genotype'] == "APOE34"
master['genotype'][index_34] = "APOE44"
#master['Geno3'] = [i.partition('HN')[0] for i in  master['Genotype'] ]

#index_HN = [ "HN" in i for i in  master['Genotype'] ]
#master['HN'] = master['Genotype']
#master['HN'][index_HN] = "HN" 
#master['HN'][[not i for i in index_HN]] = "Basic" 




#age_cat
#median = np.nanmedian(master['Age_Months'] )
#index_age = [ i > median for i in  master['Age_Months'] ]
#master['Age_cat'] = master['Age_Months']
#master['Age_cat'][index_age] = "Old"+"_" + str(np.nanmedian(master['Age_Months']))
#master['Age_cat'][[not i for i in index_age]] = "Young"+ "_" + str(np.nanmedian(master['Age_Months']))
#master['Age_cat'][np.where(master['Age_Months'].isna())[0]] = np.NaN # set the nan value back 



#define all possible cells
level_fctr_1 = np.unique(master[Factor1])
#remove_index = np.where([ "APOE" not in i for i in  level_fctr_1  ])
#level_fctr_1= np.delete(level_fctr_1,remove_index)
size_fctr_1 = len(level_fctr_1)
level_index_1 = range(1,size_fctr_1+1)



master[Factor2] = master[Factor2].str.strip()
level_fctr_2 = np.unique(master[Factor2])
size_fctr_2 = len(level_fctr_2)
level_index_2= range(1,size_fctr_2+1)



#master[Factor3] = master[Factor3].str.strip()
#level_fctr_3 = pd.unique(master[Factor3])
#remove_index = np.where( pd.isnull(level_fctr_3)  )
#level_fctr_3= np.delete(level_fctr_3,remove_index)
#size_fctr_3 = len(level_fctr_3)
#level_index_3 = range(1,size_fctr_3+1)


#master[Factor4] = master[Factor4].str.strip()
#master[Factor4] = master[Factor4].astype(str)
#level_fctr_4 = np.unique(master[Factor4])
#remove_index = np.where([ "nan"  in i for i in  level_fctr_4  ])
#level_fctr_4= np.delete(level_fctr_4,remove_index)
#size_fctr_4 = len(level_fctr_4)
#level_index_4 = range(1,size_fctr_4+1)


#master[Factor5] = master[Factor5].str.strip()
#level_fctr_5 = np.unique(master[Factor5])
#size_fctr_5 = len(level_fctr_5)
#level_index_5 = range(1,size_fctr_5+1)


####change here too
design = np.array(list(itertools.product(level_index_1 ,level_index_2 )))



myfile = open('/Users/alex/brain_data/AD_DECODE/'+contrast+'_cell.txt', 'w')       


master_temp = master
for i in range(design.shape[0]):
    temp_design = design[i]-1
    master_temp = master
    nameoffactor = ""    
    for j in range(len(temp_design)):
        
        levels = globals()["level_fctr_%s"%str(j+1)]
        lvl = levels[temp_design[j]]
        nameoffactor = nameoffactor + lvl
        print(lvl)
        chosen_list = master_temp[globals()["Factor%s"%str(j+1)]] == lvl
        master_temp = master_temp.loc[chosen_list,]
        
    chosen_DWI =master_temp['MRI_Exam']
    chosen_DWI = chosen_DWI.dropna()
    #chosen_DWI = [x[:6] for x in chosen_DWI]
    common_ID = [x for x in chosen_DWI if str(x) in Current_ID]
    common_ID = [str(x) for x in common_ID]
    common_files= [ x for x in list__files if x[2:6] in common_ID]
        
    print(temp_design+1)
    myfile.writelines(str(temp_design+1))
    myfile.writelines(str(nameoffactor))
    myfile.write('\n')
    print(*["'"+root_path + x +",1'" for x in common_files], sep='\n' )
    common_paths = [root_path + x +',1' for x in common_files]
    common_paths = ' \n '.join([''.join(i) for i in common_paths])
    myfile.write(common_paths)
    myfile.write('\n')
    print('\n')
        
        
myfile.close()      






myfile = open('/Users/alex/brain_data/AD_DECODE/'+contrast+'_age.txt', 'w')       

master_temp = master
for i in range(design.shape[0]):
    temp_design = design[i]-1
    master_temp = master
    nameoffactor = ""    
    for j in range(len(temp_design)):
        
        levels = globals()["level_fctr_%s"%str(j+1)]
        lvl = levels[temp_design[j]]
        nameoffactor = nameoffactor + lvl
        print(lvl)
        chosen_list = master_temp[globals()["Factor%s"%str(j+1)]] == lvl
        master_temp = master_temp.loc[chosen_list,]
        
    chosen_DWI =master_temp['MRI_Exam']
    chosen_DWI = chosen_DWI.dropna()
    #chosen_DWI = [x[:6] for x in chosen_DWI]
    common_ID = [x for x in chosen_DWI if str(x) in Current_ID]
    common_ID = [str(x) for x in common_ID]
    common_files = [ x for x in list__files if x[2:6] in common_ID]
    common_files  = [x[2:6] for x in common_files]  
    masterID = master_temp['MRI_Exam'] 
    masterID = [str(x) for x in masterID]
    index = [masterID.index(x) for x in common_files]
    masterage= master_temp['age']
    masterage= masterage.reset_index(drop=True)
    ages = masterage[index]
    ages  = ages.to_string(index=False)
    print(temp_design+1)
    myfile.writelines(str(temp_design+1))
    myfile.writelines(str(nameoffactor))
    myfile.write('\n')
    print(*[ages], sep='\n' )
    common_paths = ages
    
    #common_paths = ' \n '.join([''.join(i) for i in common_paths])
    myfile.write(common_paths)
    myfile.write('\n')
    print('\n')
        
        
myfile.close()      






 
    