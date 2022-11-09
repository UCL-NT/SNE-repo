import os
import numpy as np
import pandas as pd
import scipy.io as sio


#-----------------------read/load functions -----------------------------#
"""
read patients quantified output from matlab folder
e.g. '/MATLAB/Lesion_Quantification_Toolkit/Test_Outputs/Test_Batch_AAL'
	 'aal_rp001_'
	 'Tract_Disconnection'
	 'aal_rp001__percent_discon_tracts.mat'
"""
def read_mat_file(file_root_dir, patient_code, data_dir, file_name):
#combine different output folder & file name
	file_path = os.path.join(file_root_dir, patient_code, data_dir)
	mat_fname = os.path.join(file_path, patient_code+file_name)
	#print(mat_fname)

	mat_contents = sio.loadmat(mat_fname)
	print('finish read ' + patient_code)

	return mat_contents

#read Tract Disconnection percentage: tract_discon, tract_name
#return pandas data frame- rows: patients, col: track name
def load_TrackDisconnect(mat_file_root_dir, patient_num):
	data_dir = 'Tract_Disconnection'
	file_name = '_percent_discon_tracts.mat'
	tract_dict = {}

	#for loop to read all 
	for i in range(1, patient_num+1):
		#different patient code
		if i < 10:
			patient_code = 'aal_rp00'+str(i)+'_'
		else:
			patient_code =  'aal_rp0'+str(i)+'_'

		mat_contents=read_mat_file(mat_file_root_dir, patient_code, data_dir, file_name)
		tract_name = mat_contents['tract_name']
		tract_discon_val = mat_contents['tract_discon']

		if i == 1:
			for j, name in enumerate(tract_name):
				tract_dict[name[0][0]] = tract_discon_val[j]
		else:
			for j, name in enumerate(tract_name):
				tract_dict[name[0][0]]= np.append(tract_dict[name[0][0]],tract_discon_val[j])

	return pd.DataFrame(data=tract_dict)


#read disconnection matrix
#return NxNxP ndarry
def load_DisconnectMatrix(mat_file_root_dir, patient_num):
	data_dir = 'Parcel_Disconnection'
	file_name = '_Yeo7100_percent_parcel_SDC.mat'

	#for loop to read all 
	for i in range(1, patient_num+1):
		#different patient code
		if i < 10:
			patient_code = 'aal_rp00'+str(i)+'_'
		else:
			patient_code =  'aal_rp0'+str(i)+'_'

		mat_contents = read_mat_file(mat_file_root_dir, patient_code, data_dir, file_name)
		discon_matrix = mat_contents['pct_sdc_matrix']

		if i == 1:
			discon_Matrix = np.array(discon_matrix)
		elif i == 2: 
			discon_Matrix = np.stack([discon_Matrix, discon_matrix], axis=-1)
		else:
			discon_Matrix = np.concatenate((discon_Matrix, discon_matrix[..., np.newaxis]), axis=-1)
	
	return discon_Matrix


#read spared (residual) connection matrix
#return NxNxP ndarray
def loadSparedConnectMatrix(mat_file_root_dir, patient_num):
	data_dir = 'Parcel_Disconnection'
	file_name = '_Yeo7100_percent_parcel_spared_SC.mat'

	#for loop to read all 
	for i in range(1, patient_num+1):
		#different patient code
		if i < 10:
			patient_code = 'aal_rp00'+str(i)+'_'
		else:
			patient_code =  'aal_rp0'+str(i)+'_'

		mat_contents = read_mat_file(mat_file_root_dir, patient_code, data_dir, file_name)
		spared_con_matrix = mat_contents['pct_spared_sc_matrix']

		if i == 1:
			spared_con_Matrix = np.array(spared_con_matrix)
		elif i == 2: 
			spared_con_Matrix = np.stack([spared_con_Matrix, spared_con_matrix], axis=-1)
		else:
			spared_con_Matrix = np.concatenate((spared_con_Matrix, spared_con_matrix[..., np.newaxis]), axis=-1)
	
	return spared_con_Matrix

