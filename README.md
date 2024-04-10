# Gitaxian-Probe

## Contents
_____________
### Planning - Serum Visions
A folder encapsulating all files about part 1: Planning.   
Contains 5 PDDL files, 1 domain, and 4 problem files.   
`SerumVisions.pddl` - Domain file containing problem specifications  
`PROBLEMFILE4.pddl` | Problem Files For 4 Separate Situations, Outlined in `GitaxianProbeReport`  
`PROBLEMFILE3.pddl` |  
`PROBLEMFILE2.pddl` |  
`PROBLEMFILE1.pddl` |  

### Networks
Contains 2 python file, 
`main.py` - Main Python File that creates, and queries the bayesian network outlined in the report  RUN THIS ONE ONLY 
`test.py` - Should not be run, used for testing, however may contain useful information for the future

### Deep learning
Folder containing all files about part 3: Deep Learning  
Contains 2 python files   
`main.py` - Main Python File to run, creates, tests and runs the deep learning module, RUN THIS ONE ONLY
`testing.py` - Testing file, should not be run, may contain useful testing however. 
`webscraper.py` - Unused web scraping python file, may be needed in the future for more complex data problems. 
`data.json` - Stores raw data 
`testing_data.json` - Stores filtered and seperated data, contains testing data. 
`training_data.json` - Stores filtered and seperated data, contains training data. 
`validation_data.json` - Stores filtered and seperated data, contains validation data. 
`training_data_labels` - Stores data labels for the data jsons, contains training labels. 
`test_data_labels.json` - Stores data labels for the data jsons, contains testing labels
`validation_data_labels.json` - Stores data labels for the data jsons, contains validation labels
`vector-text-model.keras` - The file that stores the textVectorization layer to be used in the layer() function
`vector-text-model.h5` - Unused textVectorization layer that is used as a backup
`my_model.keras` - The Keras file that stores the main deep learning model.
`default-cards.json` - A JSON file containing all information about each card.   

### Documents
Folder containing all documents about the project,   
`GitaxianProbeReport.pdf` - Report outlining all relevant information. Start here if uninitiated.   
`problem_formulation.pptx` - Slideshow containing initial problem formulation  
_________________
