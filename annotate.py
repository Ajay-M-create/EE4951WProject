# Run this as "python annotate.py"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import neurokit2 as nk
from ecgdetectors import Detectors
import math as m

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
    dist = [0] * (len(Ploc) - 1)
    '''
    for i in range(0,len(Ploc)):
        for j in range(0,len(Rloc)):
            if (Rloc[j] > Ploc[i]):
                dist += Rloc[j] - Ploc[i]
                break
    
    avg_dist = dist/len(Ploc)

    return avg_dist/400
    '''


    ### doesn't consistenly give back PR interval
    ### Look up code to calculate Pr interval with csv file
    for i in range(0,len(Ploc) - 1):
        #print("distance added: " + str(dist))
        dist[i] = Rloc[i + 1] - Ploc[i + 1]

    return (sum(dist)/(len(Ploc) - 1))/400

def visualizeSinusTac(data, R_loc, ECG, fig, axTac):
    R_locations = R_loc["ECG_R_Peaks"]
    LeadTwo = ECG.iloc[:,1][0:4000]
    time = list(range(0, len(LeadTwo)))
    #fig = plt.figure()
    #axTac = fig.add_subplot()
    graphicTac = axTac.plot(time, LeadTwo, label='DII', color = 'orange')
    axTac.annotate("Heart Rate: "+str(round(data,2))+"BPM", xy=(R_locations[1],0.5), xycoords='data', xytext=(R_locations[2], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
    axTac.set_ylim(-1.5,1.5)
    #plt.show()
    

def visualizeSinusBrac(data, R_loc, ECG, fig, axBrac):
    R_locations = R_loc["ECG_R_Peaks"]
    LeadTwo = ECG.iloc[:,1][0:4000]
    time = list(range(0, len(LeadTwo)))
    #fig = plt.figure()
    #axBrac = fig.add_subplot()
    graphicBrac = axBrac.plot(time, LeadTwo, label='DII', color = 'orange')
    axBrac.annotate("Heart Rate: "+str(round(data,2))+" BPM", xy=(R_locations[1],1.0), xycoords='data', xytext=(R_locations[2], 1.0), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
    axBrac.set_ylim(-1.5,1.5)
    #plt.show()

def visualizeAVBlock(data, R_loc, P_loc, ECG, fig, axAV):
    print(R_loc)
    print(P_loc)
    LeadTwo = ECG.iloc[:,8][0:4000]
    time = list(range(0, len(LeadTwo)))
    #fig = plt.figure()
    #ax = fig.add_subplot()
    graphic = axAV.plot(time, LeadTwo, label='DII', color = 'orange')
    axAV.annotate("PR Interval: "+str(round(data,2))+" sec", xy=(P_loc[1],0.5), xycoords='data', xytext=(R_loc[1], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
    #ax.set_ylim(-1.5,1.5)
    plt.show()

    



'''
This function needs to be complete. It takes in the gold standard results, and then confirm if they
exist, and returns whether or not it found them
'''
def arrythmias_to_test(data, ECG):
    fig = plt.figure()
    ax = fig.add_subplot()
    if (data[0] == 1):
        # do work
        PR_interval, R_Loc, P_Loc = av_block(ECG)
        print("PR_interval: " + str(PR_interval))
        print(R_Loc)
        print(P_Loc)
        visualizeAVBlock(PR_interval, R_Loc, P_Loc, ECG, fig, ax)
        #pass
    #if (data[1] == 1):
        # do work
    #if (data[2] == 1):
        # do work
    if (data[3] == 1):
        # do work
        rate, R_loc = sinus_brac(ECG)
        print("sinus brac: " + str(rate))
        visualizeSinusBrac(rate, R_loc, ECG, fig, ax)
    #if (data[4] == 1):
        # do work
    if (data[5] == 1):
        # do work  
        rate, R_loc = sinus_tac(ECG)
        print("sinus tac: " + str(rate))   
        visualizeSinusTac(rate, R_loc, ECG, fig, ax)  

    plt.show() 


def sinus_brac(ECG):
    # Extract R-peaks locations
    clean_ecg = ECG.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    rate = find_heart_rate(R_info_dict['ECG_R_Peaks'])
    if (rate < 60):
        return rate, R_info_dict
    else:
        return rate, R_info_dict

def sinus_tac(ECG):
    # Extract R-peaks locations
    clean_ecg = ECG.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    rate = find_heart_rate(R_info_dict['ECG_R_Peaks'])
    if (rate > 100):
        return rate, R_info_dict
    else:
        return rate, R_info_dict

def av_block(ECG):
    # Extract R-peaks locations
    clean_ecg = ECG.iloc[:,8][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    # Extract P-peak locations
    PQST_locations, PQST = nk.ecg_delineate(clean_ecg, R_info_dict, sampling_rate=400, method='dwt')
    P_locations = PQST['ECG_P_Peaks']
    #print(R_info_dict['ECG_R_Peaks'])
    #print(P_locations)
    plot = nk.events_plot([R_info_dict['ECG_R_Peaks'], P_locations], clean_ecg) 
    result = PR_interval(P_locations, R_info_dict['ECG_R_Peaks'])
    result = round(result, 1)
    if (result > 0.2):
        return result, R_info_dict["ECG_R_Peaks"], P_locations
    else:
        return result, R_info_dict["ECG_R_Peaks"], P_locations


    return 0

def right_block(ECG):
    return 0

def left_block(ECG):
    return 0

def atrial_fib(ECG):
    return 0

"""

### Code Control
patient_num = 34
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


### Test for Arrythmias and Visualize
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
"""