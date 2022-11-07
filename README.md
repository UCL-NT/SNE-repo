# SNE-repo
Analyses of Structural Network Efficiency

- put three python files (build_network_graph.py, part_corr.py, data_read.py) together in a folder 
- Run command line through terminal in the same folder (where you put all the python files) 

How to run build_network_graph.py
-	After getting all quantified outputs from Lesion Quantification Toolkit under Matlab, network graph and the efficiency can be built and measured through build_network_graph.py under Python
-	After running the build_network_graphy.py, a output file networkEfficiency.xlsx will be generated.
There are 4 inputs to put in the command line: 
1.	quantified output directory (where you put the outputs from Matlab)
2.	excel file that saves the network parcel index (what structural parcels are included in each network)
3.	participants number
4.	threshold of remained connections
run command line: python build_network_graph.py input1 input2 input3 input4

Example command:

python build_network_graph.py /MATLAB/Lesion_Quantification_Toolkit/Test_Outputs aal_parcels.xlsx 36 70.0

How to run part_corr.py
-	After running the part_corr.py, a output file saving all results (r values and p values) will be generated.
There are 4 inputs to put in the command line: 
1.	excel file that saves the variables (e.g. networkEfficiency.xlsx)
2.	excel file that saves the corresponding variables you want to test (e.g. PCA factors in this case)
3.	excel file that saves control variable
4.	output file name you want
5.	participants number

run command line: python part_corr.py input1 input2 input3 input4 input5

Example command

python part_corr.py networkEfficiency.xlsx pca_factors.xlsx control.xlsx output_file 36

python part_corr.py tractDisconnect.xlsx pca_factors.xlsx control.xlsx output_file 36
