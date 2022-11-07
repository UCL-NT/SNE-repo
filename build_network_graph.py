import os
import sys
import numpy as np
import pandas as pd
import networkx as nx
import dataRead as DR
from matplotlib import pyplot as plt
"""
build_network_graph.py
-- build the graph based on AAL structural parcellation
-- measure network efficiency

"""
#input: NxN mat, network node list
#output: dictionary 
def findNetworkEfficiencyAverage(adj_mat, node_list):
	G = nx.Graph(adj_mat, nodetype=int)

	cnt = 0
	total = 0
	for i in range(len(node_list)):
		for j in range(i+1, len(node_list)):
			cnt+=1
			total+=nx.efficiency(G, node_list[i], node_list[j])

	network_eff=total/cnt
	
	return network_eff
#-------------------------------------------------------------#

def main():

	print("python graph_Analyse.py quantified_data_dir networkAAL_file patient_number threashold")

	#read inputs
	mat_file_root_dir = sys.argv[1]
	file_networkAAL = sys.argv[2]
	patient_size = sys.argv[3]
	remain_threashold = sys.argv[4]

	patient_num = int(patient_size)
	threashold_num = float(remain_threashold)

	network_AALparcels = pd.read_excel(file_networkAAL, header=0) #read all the network node index
	print(network_AALparcels)
	networks_list=list(network_AALparcels.columns.values) #get all network names 

	data_spared_con_matrix = DR.loadSparedConnectMatrix(mat_file_root_dir, patient_num)

	#------------------------measure structural network efficiency -------------
	network_efficiency_df = pd.DataFrame(columns = networks_list)
	
	for i in range(patient_num):
		pat_adjMat = np.where(data_spared_con_matrix[:, :, i] > threashold_num, 1, 0)
		tmp_list = []
		for network in networks_list:
			nodes = network_AALparcels[network_AALparcels[network].notna()]
			tmp_list.append(findNetworkEfficiencyAverage(pat_adjMat, nodes[network].astype(int)))
		network_efficiency_df.loc[i] = tmp_list

	network_efficiency_df.index = np.arange(1, len(network_efficiency_df)+1)
	network_efficiency_df.to_excel('networkEfficiency.xlsx', index=True)

if __name__ == "__main__":
    main()



