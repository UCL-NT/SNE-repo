import sys
import math
import pandas as pd
import numpy as np

import scipy.stats as stats
from sklearn.utils.validation import check_random_state
from sklearn.preprocessing import StandardScaler


def permtest_partial_corr(df, node, col, compare_num, cov, n_perm=10000, seed=0):
    """
    Same correlation permutation test process as in Netneurotools and NBS toolbox
    
    """
    x = df[node].to_numpy()
    y = df[col].to_numpy()
    true_corr = partial_corr(x, y, cov)
    abs_true = abs(true_corr)

    permutations = 1
    rs = check_random_state(seed)

    max_perm_corr = np.zeros(n_perm)
    for perm in range(n_perm):
        ap = y[rs.permutation(len(y))]
        perm_corr = np.zeros((compare_num,))
        for i in range(compare_num):
            if i != df.columns.get_loc(node):
                perm_corr[i] = abs(partial_corr(df.iloc[:, i].to_numpy(), ap, cov))
        max_perm_corr[perm] = np.max(perm_corr)
        permutations += (max_perm_corr[perm] >= abs_true)

    pvals = permutations / n_perm

    return true_corr, pvals

#-------------------------------------------------------------#
def partial_corr(x, y, control):
    
    rxy = stats.spearmanr(x, y)[0]
    ryc = stats.spearmanr(y, control)[0]
    rxc = stats.spearmanr(x, control)[0]

    p_cor = (rxy-ryc*rxc)/(math.sqrt(1-ryc**2)*math.sqrt(1-rxc**2))
        
    return p_cor

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

	df_test = pd.concat([predictor_data, outcomes_data], axis = 1)
	print(df_test)
	features=list(df_test.columns.values)
	x = df_test.loc[:, features].values
	x=StandardScaler().fit_transform(x)
	df_test = pd.DataFrame(x, columns=features)
	print(df_test)
	for node in nodes:
		print(node)
		for col in factors:
			print(col)
			r_val, p_val  = permtest_partial_corr(df_test, node, col, len(nodes)-1, covariate['Lesion_Vol'])
			resultCorrPredictor_df[col+'_r'][node] = r_val
			resultCorrPredictor_df[col+'_p'][node] = p_val

	output_file = output_file_name+'.xlsx'
	resultCorrPredictor_df.to_excel(output_file, index=True)


if __name__ == "__main__":
    main()
