# hill-climb_path_gen
Meta-heuristic approach towards robot-assisted path generation in wilderness search and rescue domain (WiSAR).

## Run program by issuing following command: 

	python path_plan.py -f <location of input file>

eg. python path_plan.py -f heatmap_1.txt

* Program generates two files in the same folder, named: 
  1) <input file name\>_complete_coverage.txt
  2) <input file name\>_most_efficient.txt
  
### Watch the explanation here:  

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/LskhySoaqz4/0.jpg)](https://www.youtube.com/watch?v=LskhySoaqz4)

### Notes:
* To check for complete coverage, please check against file 1.

* The folder 'outputs' contains the respective output files for heatmap_1 and heatmap_2

* The folder 'animations' contains the path animations for each heatmap. Maybe you can use them to verify that high-probability nodes are   visted first. 

PS: 
1) Program and output were generated on a Unix machine and might not display properly on Windows. Please use an editor that can parse the files properly, like notepad++.
2) Program assumes that 'numpy' and 'matplotlib' are already installed.
