import h5py
import numpy as np

path = 'dataset/2017-05-12_batchdata_updated_struct_errorcorrect.mat'
f = h5py.File(path, 'r')
batch = f['batch']

cell0_summary_ref = batch['summary'][0][0]
cell0_summary = f[cell0_summary_ref]

for key in cell0_summary.keys():
    val = cell0_summary[key]
    print(f"{key}: shape={val.shape}, dtype={val.dtype}, sample={val[:3].flatten()}")