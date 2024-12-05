# SNE-repo
## Analyses of Structural Network Efficiency
from paper "Uncovering Hidden Pathways: Structural Brain Networks Underpinning Connected Speech in Post-Stroke Aphasia" (2024 in process)

### -Environment-
  + python 3.9
  + installed packages: numpy, scipy, pandas, sklearn, networkx

### -Ready for these files-
  + Functional-defined network: excel file including the functional-defined networks and corresponding AAL parcels (see network_AALindex.xlsx)
  + Behavioural scores: excel file including all tested behvaioural scores of each participant (see behaviour_Speech.xlsx)
  + Lesion volume: excel file including lesion volume of each participant (see control.xlsx)
  + All quantified outputs from Lesion Quantification Toolkit under Matlab (we provide ours in Test_Batch_AAL folder)

### Steps:
1. Put python files together in the same folder, here you can just go to main folder
2. Run command line through terminal in the same folder (i.e. where you put all the python files) 
    1. run build_network_graph.py
    2. run part_corr.py
Please see the below example command-
#### Run build_network_graph.py
##### *After running build_network_graphy.py, an output file networkEfficiency.xlsx will be generated in the same folder.
  There are 4 inputs to put in the command line: 
  + quantified output directory (where you put the quantified outputs)
  + excel file with network parcel index (e.g. network_AALindex.xlsx)
  + total number of participants
  + threshold of residual connections

##### Example command:
  ###### python build_network_graph.py ../Test_Batch_AAL ../networkEff_AALindex.xlsx 36 70.0
  

#### Run part_corr.py
##### *After running part_corr.py, an output file saving all results (r values and p values) will be generated.
There are 4 inputs to put in the command line: 
+ excel file with the efficiency variables (e.g. networkEfficiency.xlsx, generated from last step)
+ excel file with the corresponding behavioural variables (e.g. speech production performance in this case)
+ excel file with control variable (e.g. lesion volume in this case)
+ output file name 

##### Example command:
  ###### python part_corr.py networkEfficiency.xlsx ../behaviour_Speech.xlsx ../control.xlsx output_file

