#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:11:35 2024

@author: alex
"""

import glob
import os

# Set the common directory path
common_dir = '/Users/alex/brain_data/AD_DECODE/'

# Set the prefixes you're interested in

prefix_1 = "jac"
prefix_2 = "fa"
prefix_3 = "QSM"
prefix_4 = "CBF"

# Initialize file lists for the specified prefixes
files_prefix_1 = []
files_prefix_2 = []
files_prefix_3 = []
files_prefix_4 = []

# Define the directory path for each prefix
prefix_1_dir = common_dir + prefix_1 + '_zscored_u/smoothed/'
prefix_2_dir = common_dir + prefix_2 + '_zscored_u/smoothed/'
prefix_3_dir = common_dir + prefix_3 + '_zscored_u/smoothed/'
prefix_4_dir = common_dir + prefix_4 + '_zscored_u/smoothed/'

# Use glob to find files matching the pattern in the specified directories
files_prefix_1 = glob.glob(prefix_1_dir + '*.nii*')
files_prefix_2 = glob.glob(prefix_2_dir + '*.nii*')
files_prefix_3 = glob.glob(prefix_3_dir + '*.nii*')
files_prefix_4 = glob.glob(prefix_4_dir + '*.nii*')

# Extract the base filenames for both prefixes
base_filenames_prefix_1 = {os.path.basename(file)[:6] for file in files_prefix_1}
base_filenames_prefix_2 = {os.path.basename(file)[:6] for file in files_prefix_2}
base_filenames_prefix_3 = {os.path.basename(file)[:6] for file in files_prefix_3}
base_filenames_prefix_4 = {os.path.basename(file)[:6] for file in files_prefix_4}

# Find common base filenames based on the first 6 characters
common_base_filenames = base_filenames_prefix_2.intersection(base_filenames_prefix_3)

common_base_filenames_4 = ((base_filenames_prefix_1.intersection(base_filenames_prefix_2)).intersection(base_filenames_prefix_3)).intersection(base_filenames_prefix_4)

# Print or process the common files
print(f"Common Files with First 6 Characters between {prefix_2} and {prefix_3}:")
for common_base_filename in common_base_filenames:
    # Construct the full paths using the common base filename
    common_files_prefix_2 = [file for file in files_prefix_2 if os.path.basename(file).startswith(common_base_filename)]
    common_files_prefix_3 = [file for file in files_prefix_3 if os.path.basename(file).startswith(common_base_filename)]
    
    # Print or process the common files for each prefix
    for file in common_files_prefix_2:
        print(f"{prefix_2}: {file}")
    for file in common_files_prefix_3:
        print(f"{prefix_3}: {file}")
        
        
myfile = open('/Users/alex/brain_data/AD_DECODE/common_runnos.csv', 'w')           
      
printed = ' \n '.join([''.join(i) for i in common_base_filenames])  
myfile.write(printed)

myfile.close()      


# Count the number of common base filenames
num_common_base_filenames = len(common_base_filenames)

# Count the number of common base filenames
num_common_base_filenames4 = len(common_base_filenames)

# Print the count
print(f"Number of Common Base Filenames between {prefix_2} and {prefix_3}: {num_common_base_filenames}")

#########################################################################

