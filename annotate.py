# Run this as "python annotate.py"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import neurokit2 as nk
from ecgdetectors import Detectors

### Takes in the location of the peaks, and calculates the heart rate
### Combining this with the number of pioints can easily tell us the heart rate
### We can easily show two abnormalities now
def find_RR_distance(data):
    avg = data[1] - data[0]
    if (len(data) < 3):
        return avg

    for x in range(1,len(data) - 1):
        newDist = data[x + 1] - data[x]
        avg = (avg + newDist)/2
        
    return avg



patient_num = 2
plots_on = True




patient_ecg = 'Patient_ECGs/patient' + str(patient_num) + '.csv'
classifications = 'Our_Files/ecg_output.csv'
#correct_dianosis = 'Our_Files/gold_standard.csv'   # Uncomment when able to get updated repo
data = pd.read_csv(patient_ecg)


diagnosis = pd.read_csv(classifications)
diagnosis = diagnosis.T
patient_prob = diagnosis[patient_num]
probs_list = list(patient_prob)
print(probs_list)

################################################ experimental -- neurokit2
# Show All wave annotation
# Retrieve ECG data from data folder
# Use given function to get cleaner signal
#clean_ecg = nk.ecg_clean(data.iloc[:,5][0:4000])
clean_ecg = data.iloc[:,1][0:5000]
# Extract R-peaks locations
R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
# Extract PQST Locations
'''
PQST_locations, PQST = nk.ecg_delineate(clean_ecg, 
                                 R_info_dict['ECG_R_Peaks'], 
                                 sampling_rate=400, 
                                 method="peak", 
                                 show=True, 
                                 show_type='peaks')
                                 '''

PQST_locations, PQST = nk.ecg_delineate(clean_ecg)
## Plot information

plot = nk.events_plot([R_info_dict['ECG_R_Peaks'],
                        PQST['ECG_T_Peaks'], 
                        PQST['ECG_P_Peaks'], 
                        PQST['ECG_Q_Peaks'], 
                        PQST['ECG_S_Peaks']], clean_ecg)
                        



#Find RR_distance
print(find_RR_distance(R_info_dict['ECG_R_Peaks']))
##############################################################################

################################################ experimental -- ecgdetectors
'''fs=100 # sample freq
detectors = Detectors(fs)
heartbeat = data
r_peaks_pan = detectors.swt_detector(heartbeat.iloc[:,5][0:4000])
r_peaks_pan= np.asarray(r_peaks_pan)

plt.plot(heartbeat.iloc[:,2][0:4000])
plt.plot(r_peaks_pan,heartbeat.iloc[:,2][0:4000][r_peaks_pan], 'ro')
'''
##############################################################################

lead_0 = list(data["0"])
lead_1 = list(data["1"])
lead_2 = list(data["2"])
lead_3 = list(data["3"])
lead_4 = list(data["4"])
lead_5 = list(data["5"])
lead_6 = list(data["6"])
lead_7 = list(data["7"])
lead_8 = list(data["8"])
lead_9 = list(data["9"])
lead_10 = list(data["10"])
lead_11 = list(data["11"])

if plots_on == True:
    time = list(range(0, len(lead_0)))
    #fig = plt.figure(figsize=(18, 12))
    fig, axes = plt.subplots(nrows=6, ncols=2, figsize=(18,12))

    axes[0,0].plot(time, lead_0, label='DI', color = 'red')
    axes[0,0].set_title('Lead 0')
    axes[1,0].plot(time, lead_1, label='DII', color = 'orange')
    axes[1,0].set_title('Lead 1')
    axes[2,0].plot(time, lead_2, label='DIII')
    axes[2,0].set_title('Lead 2')
    axes[3,0].plot(time, lead_3, label='AVR', color = 'green')
    axes[3,0].set_title('Lead 3')
    axes[4,0].plot(time, lead_4, label='AVL', color = 'orchid')
    axes[4,0].set_title('Lead 4')
    axes[5,0].plot(time, lead_5, label='AVF', color = 'slateblue')
    axes[5,0].set_title('Lead 5')
    axes[0,1].plot(time, lead_6, label='V1', color = 'magenta')
    axes[0,1].set_title('Lead 6')
    axes[1,1].plot(time, lead_7, label='V2', color = 'deeppink')
    axes[1,1].set_title('Lead 7')
    axes[2,1].plot(time, lead_8, label='V3', color = 'wheat')
    axes[2,1].set_title('Lead 8')
    axes[3,1].plot(time, lead_9, label='V4', color = 'firebrick')
    axes[3,1].set_title('Lead 9')
    axes[4,1].plot(time, lead_10, label='V5', color = 'dimgray')
    axes[4,1].set_title('Lead 10')
    axes[5,1].plot(time, lead_11, label='V6', color = 'crimson')
    axes[5,1].set_title('Lead 11')

    plt.tight_layout()
    plt.show()

classification_max = probs_list.index(max(probs_list))
print(classification_max)

if(max == 0): #1dAvB
    pass
if(max == 1): #RBBB
    pass
if(max == 2): #LBBB
    pass
if(max == 3): #bradycardia
    pass
if(max == 4): #Atrial Fibrilation
    pass
if(max == 5): #Tachycardia
    pass