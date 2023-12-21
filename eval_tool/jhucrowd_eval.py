##########################################################################
# Code to evaluate results for JHU-CROWD++ dataset
# Author - Vishwanath Sindagi
##########################################################################


import numpy as np
import os
import argparse



def get_errors(count_vec):
	count_vec = np.array(count_vec)
	diff = abs(count_vec[:,0] - count_vec[:,1])	
	diff_norm = diff/(1+count_vec[:,0])
	mae = format(np.round(diff.mean(),2),'7.1f')
	mse = format(np.round(np.sqrt((diff*diff).mean()),2),'7.1f')

	return mae, mse



def compute_errors(path_dataset, pred_file, mode):
	 
	gt_file = os.path.join(path_dataset, mode,'image_labels.txt')

	gt = {}
	pred = {}

	with open(gt_file, "r") as f:
		lines = f.readlines()

		for line in lines:
			words = line.strip().split(',')
			gt[words[0]] = {}
			gt[words[0]]['count'] = float(words[1])
			gt[words[0]]['weather'] = float(words[3])


	with open(pred_file, "r") as f:
		lines = f.readlines()
		for line in lines:
			words = line.strip().split(',')			
			 
			pred[words[0].split('.')[0]] = float(words[1])


	overall = []
	fog = []
	rain = []
	snow = []
	low = []
	med = []
	high = []
	weather = []
	distractor = []	
	for key in sorted(gt.keys()):		
		if key in pred.keys():
			overall.append([gt[key]['count'] , pred[key]])
			if gt[key]['weather'] == 1 :
				fog.append([gt[key]['count'] , pred[key]])
			if gt[key]['weather'] == 2 :
				rain.append([gt[key]['count'] , pred[key]])
			if gt[key]['weather'] == 3 :
				snow.append([gt[key]['count'] , pred[key]])

			if gt[key]['weather'] == 1 or  gt[key]['weather'] == 2 or gt[key]['weather'] == 3:
				weather.append([gt[key]['count'] , pred[key]])

			if gt[key]['count'] < 50:
				low.append([gt[key]['count'] , pred[key]])
			elif gt[key]['count'] < 500:
				med.append([gt[key]['count'] , pred[key]])
			else:
				high.append([gt[key]['count'] , pred[key]])
		else:
			print('Error: file not found in prediction. Please ensure "mode" is selected appropriately.')
			exit(0)
	

	
	mae_overall, mse_overall = get_errors(overall)
	mae_fog, mse_fog = get_errors(fog)
	mae_rain, mse_rain = get_errors(rain)
	mae_snow, mse_snow = get_errors(snow)
	mae_weather, mse_weather = get_errors(weather)
	mae_low, mse_low = get_errors(low)
	mae_med, mse_med = get_errors(med)
	mae_high, mse_high = get_errors(high) 
	 
	print(''.ljust(20),'mae_low',',','mse_low',',','mae_med',',','mse_med',',',\
		'mae_high',',','mse_high',',','mae_weather',',','mse_weather',',','mae_overall',',','mse_overall')

	print(pred_file.split('/')[-1].split('.')[0].ljust(20),',',mae_low,',',mse_low,',',mae_med,',',mse_med,',',\
		mae_high,',',mse_high,',',mae_weather.rjust(12),',',mse_weather.rjust(12),',',mae_overall.rjust(10),',',mse_overall.rjust(10))


 

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('path_dataset', type=str,
                   help='path to jhu_crowd_v2 dataset')
parser.add_argument('pred_file', type=str,
                   help='path to the prediction file')
parser.add_argument('mode', type=str,
                    help='val/test')

args = parser.parse_args()


compute_errors(args.path_dataset, args.pred_file, args.mode)

