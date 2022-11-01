# Run this as "python annotate.py"

import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
import neurokit2 as nk
#from ecgdetectors import Detectors

### Takes in the location of the peaks, and calculates the heart rate
### Combining this with the number of pioints can easily tell us the heart rate
### We can easily show two abnormalities now
def find_heart_rate(data):
    avg = data[1] - data[0]
    if (len(data) < 3):
        return avg

    for x in range(1,len(data) - 1):
        newDist = data[x + 1] - data[x]
        avg = (avg + newDist)/2

    ans = (1/avg)*(400)*(60)
    return ans

def PR_interval(Ploc, Rloc):
    dist = 0
    for i in range(0,len(Ploc)):
        for j in range(0,len(Rloc)):
            if (Rloc[j] > Ploc[i]):
                dist += Rloc[j] - Ploc[i]
                break

    avg_dist = dist/len(Ploc)

    return avg_dist/400

'''
This function needs to be complete. It takes in the gold standard results, and then confirm if they
exist, and returns whether or not it found them
'''
def arrythmias_to_test(data, ECG):
    if (data[0] == 1):
        # do work
        av_block(ECG)
    #if (data[1] == 1):
        # do work
    #if (data[2] == 1):
        # do work
    if (data[3] == 1):
        # do work
        print("sinus bracc: " + str(sinus_brac(ECG)))
    #if (data[4] == 1):
        # do work
    if (data[5] == 1):
        # do work
        print("sinus tac: " + str(sinus_tac(ECG)))


def sinus_brac(ECG):
    # Extract R-peaks locations
    clean_ecg = data.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    if (find_heart_rate(R_info_dict['ECG_R_Peaks']) < 60):
        return 1
    else:
        return 0

def sinus_tac(ECG):
    # Extract R-peaks locations
    clean_ecg = data.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    if (find_heart_rate(R_info_dict['ECG_R_Peaks']) > 100):
        return 1
    else:
        return 0

def av_block(ECG):
    # Extract R-peaks locations
    clean_ecg = data.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    # Extract P-peak locations
    PQST_locations, PQST = nk.ecg_delineate(clean_ecg)
    P_locations = PQST['ECG_P_Peaks']
    #print(R_info_dict['ECG_R_Peaks'])
    #print(P_locations)
    plot = nk.events_plot([R_info_dict['ECG_R_Peaks'], P_locations], clean_ecg)
    result = PR_interval(P_locations, R_info_dict['ECG_R_Peaks'])
    print(result)


    return 0

def right_block(ECG):
    return 0

def left_block(ECG):
    return 0

def atrial_fib(ECG):
    return 0



### Code Control
patient_num = 13
plots_on = True



### Set up patient data
patient_ecg = 'Patient_ECGs/patient' + str(patient_num) + '.csv'
data = pd.read_csv(patient_ecg)

### Extract correct diagnosis
gold_standard = 'Our_Files/gold_standard.csv'
correct_diagnosis = pd.read_csv(gold_standard)
correct_diagnosis = correct_diagnosis.T
gold_standard_result = correct_diagnosis[patient_num - 1]
diagnosis_list = list(gold_standard_result)
print(diagnosis_list)



### Extract Model Output of Probabilities
classifications = 'Our_Files/ecg_output.csv'
diagnosis = pd.read_csv(classifications)
diagnosis = diagnosis.T
patient_prob = diagnosis[patient_num]
probs_list = list(patient_prob)
print(probs_list)


### Test for Arrythmias
arrythmias_to_test(diagnosis_list, data)


################################################ experimental -- neurokit2
# Show All wave annotation
# Retrieve ECG data from data folder
#temp = data.iloc[:,1][0:4000]
#clean_ecg = nk.ecg_clean(temp, sampling_rate=400)

# Extract R-peaks locations
#R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
# Extract PQST Locations

### This plot only the R peak locations
'''
PQST_locations, PQST = nk.ecg_delineate(clean_ecg, 
                                 R_info_dict['ECG_R_Peaks'], 
                                 sampling_rate=400, 
                                 method="peak", 
                                 show=True, 
                                 show_type='peaks')
                                 '''
'''
## This plots all the peaks locations of interst
PQST_locations, PQST = nk.ecg_delineate(clean_ecg)

plot = nk.events_plot([R_info_dict['ECG_R_Peaks'],
                        PQST['ECG_T_Peaks'], 
                        PQST['ECG_P_Peaks'], 
                        PQST['ECG_Q_Peaks'], 
                        PQST['ECG_S_Peaks']], clean_ecg)

plot = nk.events_plot([R_info_dict['ECG_R_Peaks'],
                        PQST['ECG_P_Peaks']], clean_ecg)

'''

#Find RR_distance
#print(find_heart_rate(R_info_dict['ECG_R_Peaks']))
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