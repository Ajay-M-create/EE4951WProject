Project Title: Annotation of Abnormal Electrocardiogram Waveforms Diagnosed by Machine Learning

Date: 12/22/2022

Participants: Ajay Manicka, John Franklin, Tanner Jack, Elias Caceres, Stephanie Ye

Participants: Advisor: Professor Gerald Sobelman

Project Folder Contents:
ReadME: Explanation of necessary Python3 libraries to install and how to run code. Also contains information containing the initial ML repository and what the code does at a high level.
99.png: One example output from our Machine Learning model.
556.png: Another example from our Machine Learning model.
main.py: Entry point of code which executes modules in annotateTest.py to demonstrate functionality of code. Currently cycles through about 30 different ECGs every 5 seconds to showcase its effectiveness through a demonstration.
annotateTest.py: The actual meat of the code where python libraries are leveraged to create annotations dynamically for each arrhythmia.
Patient_ECGs folder: Contains 800+ patient ECGs reserved as test data for the trained ML model.
Our_Files: Contains two files called ecg_output.csv and gold_standard.csv. ecg_output.csv has a list of arrhythmia prescence probabilities as an array where each array element indicates the probability that each arrhythmia is present. the array order is delineated at the top. gold_standard.csv contains the actual arrhythmias present in each ECG according to several health professionals with all confirm the result.

All code is available on GitHub here: https://github.com/Ajay-M-create/EE4951WProject