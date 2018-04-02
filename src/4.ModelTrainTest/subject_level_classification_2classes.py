
import os
import re
import csv
import pickle
import tflearn
import numpy as np


def get_pkls(testset):
  all_pkls = []
  for root,dirs,files in os.walk(testset):
    if files:
      for ff in files:
        if re.search(r'.pkl', ff):
          all_pkls.append(os.path.join(root, ff))

  return all_pkls


def evaluate_subject(model, pklfile):
  with open(pklfile, 'rb') as infile:
    sbj_data = pickle.load(infile)

  has_label = sbj_data.has_key('label')

  data_id  = sbj_data['id']
  if has_label:
    data_lab = sbj_data['label']
  data_img = sbj_data['data'] / 255.0
  print data_id

  # NL, AD
  lab_pred_list   = [0, 0]
  slice_pred_list = []
  num_right_slice = 0

  for ii in xrange(len(data_img)):
    ## There is a bug in predict_label, use predict instead
    #slice_pred_lab = model.predict_label(data_img[ii:ii+1])[0,0]

    slice_pred_lab = np.argmax(model.predict(data_img[ii:ii+1])[0])
    assert (0 == slice_pred_lab) or (1 == slice_pred_lab)

    lab_pred_list[slice_pred_lab] = lab_pred_list[slice_pred_lab] + 1
    slice_pred_list.append(slice_pred_lab)

    if has_label and slice_pred_lab == data_lab:
      num_right_slice = num_right_slice + 1

  sbj_pred_lab = np.argmax(lab_pred_list)
  if has_label:
    if sbj_pred_lab == data_lab:
      sbj_pred_right = 1
    else:
      sbj_pred_right = 0

  if has_label:
    retval = {
      'ID':data_id, 
      'EXP_RES':data_lab, 
      'NUM_SLICE':len(data_img), 
      'PRED_LABS':lab_pred_list, 
      'ACT_RES':sbj_pred_lab, 
      'PRED_RIGHT':sbj_pred_right, 
      'ACT_SLICE_RES':slice_pred_list
    }
  else:
    retval = {
      'ID':data_id,
      'NUM_SLICE':len(data_img), 
      'PRED_LABS':lab_pred_list,
      'ACT_RES':sbj_pred_lab,
      'ACT_SLICE_RES':slice_pred_list
    }

  return num_right_slice, retval, has_label


def write_test_report(sbj_result_list, report_file_name, has_label):
  ocsvfile = open(report_file_name, 'wb')
  owriter  = csv.writer(ocsvfile)

  if has_label:
    csvheader = [
      'ID', 
      'EXP_RES', 
      'NUM_SLICE', 
      'ACT_NL', 
      'ACT_AD', 
      'ACT_RES', 
      'PRED_RIGHT', 
      'ACT_SLICE_RES'
    ]
  else:
    csvheader = [
      'ID',
      'NUM_SLICE',
      'ACT_NL',
      'ACT_AD',
      'ACT_RES',
      'ACT_SLICE_RES'
    ]

  owriter.writerow(csvheader)

  for item in sbj_result_list:
    if has_label:
      contentToWrite = [
        item['ID'], 
        item['EXP_RES'], 
        item['NUM_SLICE'], 
        item['PRED_LABS'][0], 
        item['PRED_LABS'][1], 
        item['ACT_RES'], 
        item['PRED_RIGHT']
      ] + item['ACT_SLICE_RES']
    else:
      contentToWrite = [
        item['ID'], 
        item['NUM_SLICE'], 
        item['PRED_LABS'][0], 
        item['PRED_LABS'][1], 
        item['ACT_RES']
      ] + item['ACT_SLICE_RES']
    owriter.writerow(contentToWrite)

  ocsvfile.close()


def evaluate(model, testset, report_file_name):
  '''
  model: pre-trained tensorflow model
  testset: testset containing pickle files, one pkl per subject
  '''

  all_pkls = get_pkls(testset)
  print 'Number of pkl:', len(all_pkls)

  has_label = ''
  sbj_result_list = []
  num_right_slice_total = 0
  num_slice_total = 0
  for item in all_pkls:
    num_right_slice, sbj_result, has_label = evaluate_subject(model, item)
    sbj_result_list.append(sbj_result)

    num_slice_total = num_slice_total + sbj_result['NUM_SLICE']
    num_right_slice_total = num_right_slice_total + num_right_slice

  print 'sbj_result_list len:', len(sbj_result_list)
  print(has_label)
  if has_label:
    print num_right_slice_total, num_slice_total, float(num_right_slice_total) / float(num_slice_total)

  write_test_report(sbj_result_list, report_file_name, has_label)

