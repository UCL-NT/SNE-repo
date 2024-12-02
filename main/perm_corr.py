import sys
import pandas as pd
import numpy as np
import NBS_vectorized as nbs_corr


def main():
	print("python perm_corr.py predictor_data_files outcomeFactors_data_file control_file output_file")
	file_predictor = sys.argv[1]
	file_outcomes = sys.argv[2]
	file_control = sys.argv[3]
	output_file_name = sys.argv[4]

	outcomes_data = pd.read_excel(file_outcomes, header = 0, index_col=0)
	outcomes_data = outcomes_data.replace('na', np.nan)
	for col in outcomes_data.columns:
		outcomes_data[col] = outcomes_data[col].astype(float)
		outcomes_data[col].fillna(outcomes_data[col].mean(), inplace=True)
	#outcomes_data = outcomes_data.fillna(outcomes_data.mean())
	factors=list(outcomes_data.columns.values)

	predictor_data = pd.read_excel(file_predictor, index_col=0, header=0)
	predictor_data = predictor_data.fillna(predictor_data.mean()) # in case there is any missing data
	nodes=list(predictor_data.columns.values)

	covariate = pd.read_excel(file_control, index_col=0, header=0)

	#-------------run mass univariate permutation spearman partial correlation test------------
	cols =[]
	for col in factors:
		cols.append(col+'_r')
		cols.append(col+'_p')

	resultCorrPredictor_df = pd.DataFrame(columns=cols, index=nodes)

	for col in factors:
		print(col)
		p_val, r_val = nbs_corr.nbs_corr(predictor_data.to_numpy().T, outcomes_data[col].to_numpy(), covariate['Lesion_Vol'], 10000) 

		resultCorrPredictor_df[col+'_r']= r_val
		resultCorrPredictor_df[col+'_p']= p_val
    
	output_file = output_file_name+'.xlsx'
	resultCorrPredictor_df.to_excel(output_file, index=True)


if __name__ == "__main__":
    main()
