#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:58:20 2024

@author: alex
"""

'''
read all images in a directory
use otsu to threshold
use zscore on these images
use aants to smooth

'''
import nibabel as nib
import numpy as np
from skimage import filters
import glob
import os
import matplotlib.pyplot as plt
import ants

prefix='fa'
input_dir = '/Users/alex/brain_data/AD_DECODE/'+prefix+'_zscored_u/input'
output_dir = '/Users/alex/brain_data/AD_DECODE/'+prefix+'_zscored_u/smoothed/'
mask_file = '/Users/alex/brain_data/AD_DECODE/median_images/MDT_mask.nii.gz'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)



#read mask
mask_img = nib.load(mask_file)
mask_data = mask_img.get_fdata()
# Use the provided mask for thresholding
binary_mask = mask_data > 0  # Assuming your mask is binary

# Get the indices of the voxels within the mask
mask_indices = np.where(binary_mask)

# Get a list of all NIfTI files in the input directory
nii_files = glob.glob(os.path.join(input_dir, '*.nii*'))



# Process each NIfTI file
for nii_file in nii_files:
    # Load NIfTI image
    img = nib.load(nii_file)
    data = img.get_fdata()

    # Perform Otsu thresholding to create a binary mask
    #threshold_value = filters.threshold_otsu(data)
    #binary_mask = data > threshold_value
    
    # Extract the values of the voxels within the mask
    voxel_values = data[mask_indices]

    # Compute the z-score for the voxel values
    z_scores = (voxel_values - np.mean(voxel_values)) / np.std(voxel_values)

    # Create a new image with z-scores at the same voxel locations
    z_score_image = np.zeros_like(data)
    z_score_image[mask_indices] = z_scores

    # Save the z-scored result
    result_img = nib.Nifti1Image(z_score_image, img.affine)
    result_file_path = os.path.join(output_dir, os.path.basename(nii_file))
    nib.save(result_img, result_file_path)

    # Create an antsImage from the NIfTI image
    ants_image = ants.from_nibabel(result_img)

    # Smooth the image using ANTs (adjust the sigma value as needed)
    smoothed_image = ants.smooth_image(ants_image, sigma=1)

    # Convert the smoothed image back to NIfTI format
    smoothed_result_img = ants.utils.convert_nibabel.to_nibabel(smoothed_image)

    # Save the smoothed result
    smoothed_result_file_path = os.path.join(output_dir, os.path.basename(nii_file))
    nib.save(smoothed_result_img, smoothed_result_file_path)



'''
# Plot the original and smoothed slices (optional)
slice_index = result_img.shape[0] // 2 + 5

original_slice_data = img.get_fdata()[slice_index, :, :]
smoothed_slice_data = smoothed_result_img.get_fdata()[slice_index, :, :]




# Plot the slices using matplotlib
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(original_slice_data, cmap='gray', origin='lower')
plt.colorbar()
plt.title('Original Image - Slice {}'.format(slice_index))

plt.subplot(1, 2, 2)
plt.imshow(smoothed_slice_data, cmap='gray', origin='lower')
plt.colorbar()
plt.title('Smoothed Image - Slice {}'.format(slice_index))

plt.show()




os.mkdir('/Users/alex/brain_data/AD_DECODE/fa_zscored_u/masked')
#nib.save(smoothed_result_img, '/Users/alex/brain_data/AD_DECODE/fa_zscored_u/masked/smoothed_result.nii.gz')

'''


