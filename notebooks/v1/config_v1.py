import os

DATA_DIR = '../../dataset'
OUTPUT_DIR = '../../outputs/v1'

BATCH_FILES = [
    '2017-05-12_batchdata_updated_struct_errorcorrect.mat',
    '2017-06-30_batchdata_updated_struct_errorcorrect.mat',
    '2018-04-12_batchdata_updated_struct_errorcorrect.mat',
]

TRAIN_SIZE = 41
VAL_SIZE   = 43
TEST_SIZE  = 40

EKF_P0 = [2.0, 0.0]
EKF_R  = 0.01
EKF_Q  = [0.8, 0.2]

BATTERY_Q_NOMINAL = 1.1
BATTERY_R         = 0.017
BATTERY_C         = 0.1
BATTERY_RO        = 0.017
SAMPLING_TIME     = 1.0

NR_TOL      = 1e-6
NR_MAX_ITER = 100

RANDOM_SEED = 42
