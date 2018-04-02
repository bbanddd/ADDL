# -*- coding: utf-8 -*-
""" ADDL: Alzheimer's Disease Deep Learning Tool

    Preprocess Pipeline:
      Required arguments:
        -P, --preprocess      Data preprocess pipeline flag
        --P_input_data_dir P_INPUT_DATA_DIR
                              Input directory containing original NIfTI files
        --P_train_list P_TRAIN_LIST
                              Training data list file
        --P_test_list P_TEST_LIST
                              Test data list file
        --label_file LABEL_FILE
                              Label file
        --output_dir OUTPUT_DIR
                              Output directory to contain all results

      Optinal arguments:
        --P_png_low_index P_PNG_LOW_INDEX
                              Png file index from which to select, include. 
                              default 10
        --P_png_high_index P_PNG_HIGH_INDEX
                              Png file index till which to select, exclude. 
                              default 72

    Train Pipeline:
      Required arguments:
        -T, --train           Model training flag
        --T_input_data_dir T_INPUT_DATA_DIR
                              Input directory containing packed binary data
        --T_run_id T_RUN_ID   Name of tensorboard log file
        --output_dir OUTPUT_DIR
                              Output directory to contain all results

      Optinal arguments:
        --T_epoch T_EPOCH     Epoch to train network. default 300
        --T_batch_size T_BATCH_SIZE
                              Batch size. default 128
        --T_tensorboard_verbose T_TENSORBOARD_VERBOSE
                              Tensorboard verbose level, 0 | 1 | 2 | 3. 
                              default 3
        --T_tensorboard_dir T_TENSORBOARD_DIR
                              Directory to contain tensorboard log file. 
                              default /tmp/tflearn_logs/

    Inference Pipeline:
      Required arguments:
        -I, --inference       Subject level inference flag
        --I_input_test_png_dir I_INPUT_TEST_PNG_DIR
                              Input directory containing testing set png files
        --I_input_model I_INPUT_MODEL
                              Trained model
        --label_file LABEL_FILE
                              Label file
        --output_dir OUTPUT_DIR
                              Output directory to contain all results

    Preprocess and Train Pipeline:
      Required arguments:
        -P, --preprocess      Data preprocess pipeline flag
        -T, --train           Model training flag
        --P_input_data_dir P_INPUT_DATA_DIR                              
                              Input directory containing original NIfTI files
        --P_train_list P_TRAIN_LIST
                              Training data list file
        --P_test_list P_TEST_LIST
                              Test data list file
        --label_file LABEL_FILE
                              Label file
        --T_run_id T_RUN_ID   Name of tensorboard log file
        --output_dir OUTPUT_DIR
                              Output directory to contain all results

      Optinal arguments:
        --T_epoch T_EPOCH     Epoch to train network. default 300
        --T_batch_size T_BATCH_SIZE
                              Batch size. default 128
        --T_tensorboard_verbose T_TENSORBOARD_VERBOSE
                              Tensorboard verbose level, 0 | 1 | 2 | 3. 
                              default 3
        --T_tensorboard_dir T_TENSORBOARD_DIR
                              Directory to contain tensorboard log file. 
                              default /tmp/tflearn_logs/

   Preprocess and Inference Pipeline:
      Required arguments:
        -P, --preprocess      Data preprocess pipeline flag
        -I, --inference       Subject level inference flag
        --P_input_data_dir P_INPUT_DATA_DIR
                              Input directory containing original NIfTI files
        --P_study_specific_template P_STUDY_SPECIFIC_TEMPLATE
                              Study specific template file
        --I_input_model I_INPUT_MODEL
                              Trained model
        --output_dir OUTPUT_DIR
                              Output directory to contain all results

    Structure of output_dir:
      output_dir/                // Output directory specified in command line
      ├── data/                  // Original data to preprocess
      │   ├── struc/             // Preprocessed data and intermediate result
      ├── png/                   // Decomposed PNG files
      ├── png_split/             // PNG files split into train and test set
      │   ├── train/
      │   ├── test/
      ├── data_binary/           // Packed train and test data in binary
      ├── data_binary_subject/   // Packed test data in binary by subject
      ├── model/                 // Trained model parameters
      ├── ADSCReport.csv         // Subject level test report

"""


from __future__ import division, print_function, absolute_import

import os
import argparse


parser = argparse.ArgumentParser(
  description='Alzheimer\'s Disease Classification Tool')

parser.add_argument('-P', '--preprocess', action='store_true',
                    help='Data preprocess pipeline flag')

parser.add_argument('--P_input_data_dir',
                    help='Input directory containing original NIfTI files')

parser.add_argument('--P_train_list',
                    help='Training data list file')

parser.add_argument('--P_test_list',
                    help='Test data list file')

parser.add_argument('--P_study_specific_template',
                    help='Study specific template file')

parser.add_argument('--P_png_low_index', type=int, default=10,
                    help='Png file index from which to select, include. \
                          default 10')

parser.add_argument('--P_png_high_index', type=int, default=72,
                    help='Png file index till which to select, exclude. \
                          default 72')

parser.add_argument('-T', '--train', action='store_true',
                    help='Model training flag')

parser.add_argument('--T_input_data_dir',
                    help='Input directory containing packed binary data')

parser.add_argument('--T_run_id',
                    help='Name of tensorboard log file')

parser.add_argument('--T_epoch', type=int, default=300,
                    help='Epoch to train network. default 300')

parser.add_argument('--T_batch_size', type=int, default=128,
                    help='Batch size. default 128')

parser.add_argument('--T_tensorboard_verbose', type=int, default=3,
                    help='Tensorboard verbose level, 0 | 1 | 2 | 3. default 3')

parser.add_argument('--T_tensorboard_dir', 
                    default='/tmp/tflearn_logs/',
                    help='Directory to contain tensorboard log file. \
                          default /tmp/tflearn_logs/')

parser.add_argument('-I', '--inference', action='store_true',
                    help='Subject level inference flag')

parser.add_argument('--I_input_test_png_dir',
                    help='Input directory containing testing set png files')

parser.add_argument('--I_input_model',
                    help='Trained model')

parser.add_argument('--label_file',
                    help='Label file')

parser.add_argument('--output_dir',
                    help='Output directory to contain all results')

args = parser.parse_args()


preprocess       = args.preprocess
P_input_data_dir = args.P_input_data_dir
P_train_list     = args.P_train_list
P_test_list      = args.P_test_list
P_study_specific_template = args.P_study_specific_template
P_png_low_index  = args.P_png_low_index
P_png_high_index = args.P_png_high_index

train            = args.train
T_input_data_dir = args.T_input_data_dir
T_run_id         = args.T_run_id
T_epoch          = args.T_epoch
T_batch_size     = args.T_batch_size
T_tensorboard_verbose = args.T_tensorboard_verbose
T_tensorboard_dir     = args.T_tensorboard_dir

inference            = args.inference
I_input_test_png_dir = args.I_input_test_png_dir
I_input_model        = args.I_input_model

label_file = args.label_file
output_dir = args.output_dir

assert (preprocess or train or inference), \
"At least one behavior must be specified"
assert not (train and inference), "Train and inference unsupported."

g_dict_behavior = {
  1 : 'Preprocess',
  2 : 'Train',
  4 : 'Inference',
  3 : 'Preprocess and train',
  5 : 'Preprocess and inference'
}

g_behavior = 0;
if preprocess: g_behavior += 1
if train     : g_behavior += 2
if inference : g_behavior += 4


##### Command line argument validity checking
def cli_check():
  ## Preprocess
  dict_behavior1_required_argument = {
    'P_input_data_dir' : P_input_data_dir,
    'P_train_list'     : P_train_list,
    'P_test_list'      : P_test_list,
    'label_file'       : label_file,
    'output_dir'       : output_dir
  }

  ## Train
  dict_behavior2_required_argument = {
    'T_input_data_dir' : T_input_data_dir,
    'T_run_id'         : T_run_id,
    'output_dir'       : output_dir
  }

  ## Inference
  dict_behavior4_required_argument = {
    'I_input_test_png_dir' : I_input_test_png_dir,
    'I_input_model'        : I_input_model,
    'label_file'           : label_file,
    'output_dir'           : output_dir
  }

  ## Preprocessing and train
  dict_behavior3_required_argument = {
    'P_input_data_dir' : P_input_data_dir,
    'P_train_list'     : P_train_list,
    'P_test_list'      : P_test_list,
    'T_run_id'         : T_run_id,
    'label_file'       : label_file,
    'output_dir'       : output_dir
  }

  ## Preprocess and inference
  dict_behavior5_required_argument = {
    'P_input_data_dir' : P_input_data_dir,
    'P_study_specific_template' : P_study_specific_template,
    'I_input_model'    : I_input_model,
    'output_dir'       : output_dir
  }

  list_dict_behavior_required_argument = [
    {},
    dict_behavior1_required_argument,
    dict_behavior2_required_argument,
    dict_behavior3_required_argument,
    dict_behavior4_required_argument,
    dict_behavior5_required_argument
  ]

  assert g_behavior in g_dict_behavior
  print('\nBehavior:', g_dict_behavior[g_behavior])
  for k, v in list_dict_behavior_required_argument[g_behavior].items():
    assert v != None, 'missing required argument: ' + k

cli_check()

if P_input_data_dir != None and P_input_data_dir[-1] != '/':
  P_input_data_dir += '/'

if T_input_data_dir != None and T_input_data_dir[-1] != '/':
  T_input_data_dir += '/'

if T_tensorboard_dir != None and T_tensorboard_dir[-1] != '/':
  T_tensorboard_dir += '/'

if I_input_test_png_dir != None and I_input_test_png_dir[-1] != '/':
  I_input_test_png_dir += '/'

if output_dir != None and output_dir[-1] != '/':
  output_dir += '/'


##### Tools
g_binSelectData  = '../tools/data_acquire/pickupNiftiByDatalist.py'

g_dirPreprocess  = './1.DataPreprocessing/'
g_binPreprocess  = g_dirPreprocess + 'preprocess.py'
g_binPreprocessI = g_dirPreprocess + 'preprocessI.py'

g_DirDecomp      = './2.NIfTI2PNG/'
g_binDecomp      = g_DirDecomp + 'nii2Png.py'
g_binDecompNoLab = g_DirDecomp + 'nii2PngNoLabel.py'
g_binSplit       = './2.NIfTI2PNG/splitTrainTestSet.py'

g_binBinData     = './3.PNG2Binary/png2pkl.py'
g_binBinTestData = './3.PNG2Binary/png2pkl_sbjtest.py'

g_binModelTrain  = './4.ModelTrainTest/residual_network_2classes.py'
g_binInference   = './4.ModelTrainTest/residual_network_sbjrecognize_2classes.py'

##### Output directories

g_dataDir     = output_dir + 'data/'
g_dataPrepDir = g_dataDir + 'struc/'

g_pngDir      = output_dir + 'png/'
g_pngSplitDir = output_dir + 'png_split/'
g_pngSplitTrainDir = g_pngSplitDir + 'train/'
g_pngSplitTestDir  = g_pngSplitDir + 'test/'

g_binDataDir     = output_dir + 'data_binary/'
g_binTestDataDir = output_dir + 'data_binary_subject_testset/'

g_modelDir   = output_dir + 'model/'

g_testReport = output_dir + 'ADSCReport.csv'


##### Execute cmd as Linux shell command
def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)


cntEqual = 30


##### Preorpcess function when only -P or -P -T are specified
def preprocess():
  ##### Stage1: Select Data
  print('\n' + '='*cntEqual + ' ADDL Preprocess Stage1: Select Data ' + \
        '='*cntEqual)
  if os.path.exists(g_dataDir + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('rm -rf ' + g_dataDir + '*')
    cmd  = 'python ' + g_binSelectData + ' ' + P_input_data_dir + ' ' 
    cmd += P_train_list + ' ' + P_test_list + ' ' + g_dataDir
    exec_cmd(cmd)
    exec_cmd('touch ' + g_dataDir + 'DONE')

  ##### Stage2: Preprocess
  print('\n' + '='*cntEqual + ' ADDL Preprocess Stage2: Preprocessing ' + \
        '='*cntEqual)
  if os.path.exists(g_dataPrepDir + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('rm -f ' + g_dataPrepDir + '*')
    cmd  = 'python ' + g_binPreprocess + ' ' 
    cmd += g_dataDir + ' --scriptsDir ' + g_dirPreprocess
    exec_cmd(cmd)
    exec_cmd('touch ' + g_dataPrepDir + 'DONE')

  ##### Stage3: Decompose Preprocessed Data into PNG Files
  print('\n' + '='*cntEqual + \
        ' ADDL Preprocess Stage3: Decompose into PNG Files ' + '='*cntEqual)
  if os.path.exists(g_pngDir + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('rm -rf ' + g_pngDir + '*')
    cmd  = 'python ' + g_binDecomp + ' ' 
    cmd += g_dataPrepDir + ' ' + g_pngDir + ' ' 
    cmd += str(P_png_low_index) + ' ' + str(P_png_high_index) + ' ' 
    cmd += label_file + ' --scriptsDir ' + g_DirDecomp
    exec_cmd(cmd)
    exec_cmd('touch ' + g_pngDir + 'DONE')

  ##### Stage4: Split PNG files into Training and Testing Set
  print('\n' + '='*cntEqual + \
        ' ADDL Preprocess Stage4: Split into Training and Testing Set ' + \
        '='*cntEqual)
  if os.path.exists(g_pngSplitDir + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('rm -rf ' + g_pngSplitDir + '*')
    cmd  = 'python ' + g_binSplit + ' ' +  g_pngDir + ' ' 
    cmd += P_train_list + ' ' + P_test_list + ' ' + g_pngSplitDir
    exec_cmd(cmd)
    exec_cmd('touch ' + g_pngSplitDir + 'DONE')

  ##### Stage5: Pack Training and Testing Data into Binary
  print('\n' + '='*cntEqual + \
        ' ADDL Preprocess Stage5: Pack Data into Binary ' + '='*cntEqual)
  if os.path.exists(g_binDataDir + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('rm -f ' + g_binDataDir + '*')
    cmd  = 'python ' + g_binBinData + ' ' + g_pngSplitTrainDir + ' ' 
    cmd += g_binDataDir + ' ' + label_file + ' train_'
    exec_cmd(cmd)
    cmd  = 'python ' + g_binBinData + ' ' + g_pngSplitTestDir  + ' ' 
    cmd += g_binDataDir + ' ' + label_file + ' test_'
    exec_cmd(cmd)
    exec_cmd('touch ' + g_binDataDir + 'DONE')


##### Preprocess function when -P -I are specified
def preprocessI():
  ##### Stage1: Preprocess
  print('\n' + '='*cntEqual + ' ADDL PreprocessI Stage1: Preprocessing ' + \
        '='*cntEqual)
  if os.path.exists(g_dataPrepDir + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('cp -r ' + P_input_data_dir + '* ' + g_dataDir)
    exec_cmd('rm -f ' + g_dataPrepDir + '*')
    cmd  = 'python ' + g_binPreprocessI + ' ' +  g_dataDir + ' '
    cmd += P_study_specific_template + ' --scriptsDir ' + g_dirPreprocess
    exec_cmd(cmd)
    exec_cmd('touch ' + g_dataPrepDir + 'DONE')

  ##### Stage2: Decompose Preprocessed Data into PNG Files
  print('\n' + '='*cntEqual + \
        ' ADDL PreprocessI Stage2: Decompose into PNG Files ' + '='*cntEqual)
  if os.path.exists(g_pngDir + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('rm -rf ' + g_pngDir + '*')
    cmd  = 'python ' + g_binDecompNoLab + ' '
    cmd += g_dataPrepDir + ' ' + g_pngDir + ' '
    cmd += str(P_png_low_index) + ' ' + str(P_png_high_index) + ' '
    cmd += ' --scriptsDir ' + g_DirDecomp
    exec_cmd(cmd)
    exec_cmd('touch ' + g_pngDir + 'DONE')


##### Model training function
def train():
  print('\n' + '='*cntEqual + ' ADDL Train Stage1: Training Model ' + \
        '='*cntEqual)
  if os.path.exists(g_modelDir + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('rm -f ' + g_modelDir + '*')
    cmd   = 'python ' + g_binModelTrain + ' ' + T_input_data_dir + ' ' 
    cmd += str(T_epoch) + ' ' + str(T_batch_size) + ' '
    cmd += g_modelDir  + ' ' + T_run_id 
    cmd += ' --tensorboardVerbose ' + str(T_tensorboard_verbose) 
    cmd += ' --tensorboardDir ' + T_tensorboard_dir
    exec_cmd(cmd)
    cmd = 'mv ' + g_modelDir[:-1] + '-* ' + g_modelDir
    exec_cmd(cmd)
    exec_cmd('touch ' + g_modelDir + 'DONE')


##### Subject level classification function
def inference(input_test_png_dir):
  ##### Stage1: Pack Testing Data into Binary
  print('\n' + '='*cntEqual + \
        ' ADDL Inference Stage1: Pack Data into Binary by Subject ' + \
        '='*cntEqual)
  if os.path.exists(g_binTestDataDir  + 'DONE'):
    print('Already done. Skip.')
  else:
    exec_cmd('rm -rf ' + g_binTestDataDir + '*')
    cmd  = 'python ' + g_binBinTestData + ' ' 
    cmd += input_test_png_dir + ' ' + g_binTestDataDir 
    if label_file != None:  
      cmd += ' --labelFile ' + label_file
    exec_cmd(cmd)
    exec_cmd('touch ' + g_binTestDataDir + 'DONE')

  ##### Stage2: Subject Level Classification
  print('\n' + '='*cntEqual + \
        ' ADDL Inference Stage2: Subject Level Classification ' + \
        '='*cntEqual)
  if os.path.exists(g_testReport):
    print('Already done. Skip.')
  else:
    cmd  = 'python ' + g_binInference + ' ' 
    cmd += g_binTestDataDir + ' ' + I_input_model + ' ' + g_testReport
    exec_cmd(cmd)
  print('\nCheck \'%s\' for test report.' % (g_testReport))


##### main()

## Initialize output directory
g_dirs = list([
  output_dir,
  g_dataDir,
  g_pngDir,
  g_pngSplitDir,
  g_binDataDir,
  g_binTestDataDir,
  g_modelDir
])

for dd in g_dirs:
  if not os.path.exists(dd): exec_cmd('mkdir ' + dd)

if 1 == g_behavior:
  preprocess()
elif 2 == g_behavior:
  train()
elif 4 == g_behavior:
  inference(I_input_test_png_dir)
elif 3 == g_behavior:
  preprocess()
  T_input_data_dir = g_binDataDir
  train()
elif 5 == g_behavior:
  preprocessI()
  inference(g_pngDir)
else:
  print('\nImpossible\n')


exit(0)

