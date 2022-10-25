# Run this as "python annotate.py"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import neurokit2 as nk
from ecgdetectors import Detectors



patient_num = 1
plots_on = True




patient_ecg = 'Patient_ECGs/patient' + str(patient_num) + '.csv'
classifications = 'Our_Files/ecg_output.csv'
data = pd.read_csv(patient_ecg)


diagnosis = pd.read_csv(classifications)
diagnosis = diagnosis.T
patient_prob = diagnosis[patient_num]
probs_list = list(patient_prob)
print(probs_list)

################################################ experimental -- neurokit2
# Retrieve ECG data from data folder
#ecg_signal = nk.data(dataset='Patient_ECGs/patient2' + str(patient_num))
# Extract R-peaks locations
#_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=1000)
#plot = nk.events_plot(rpeaks['ECG_R_Peaks'], ecg_signal)
##############################################################################

################################################ experimental -- ecgdetectors
fs=100 # sample freq
detectors = Detectors(fs)
heartbeat = data
r_peaks_pan = detectors.swt_detector(heartbeat.iloc[:,5][0:4000])
r_peaks_pan= np.asarray(r_peaks_pan)

plt.plot(heartbeat.iloc[:,2][0:4000])
plt.plot(r_peaks_pan,heartbeat.iloc[:,2][0:4000][r_peaks_pan], 'ro')
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

    axes[0,0].plot(time, lead_0, label='lead_0', color = 'red')
    axes[0,0].set_title('Lead 0')
    axes[1,0].plot(time, lead_1, label='lead_1', color = 'orange')
    axes[1,0].set_title('Lead 1')
    axes[2,0].plot(time, lead_2, label='lead_2')
    axes[2,0].set_title('Lead 2')
    axes[3,0].plot(time, lead_3, label='lead_3', color = 'green')
    axes[3,0].set_title('Lead 3')
    axes[4,0].plot(time, lead_4, label='lead_4', color = 'orchid')
    axes[4,0].set_title('Lead 4')
    axes[5,0].plot(time, lead_5, label='lead_5', color = 'slateblue')
    axes[5,0].set_title('Lead 5')
    axes[0,1].plot(time, lead_6, label='lead_6', color = 'magenta')
    axes[0,1].set_title('Lead 6')
    axes[1,1].plot(time, lead_7, label='lead_7', color = 'deeppink')
    axes[1,1].set_title('Lead 7')
    axes[2,1].plot(time, lead_8, label='lead_8', color = 'wheat')
    axes[2,1].set_title('Lead 8')
    axes[3,1].plot(time, lead_9, label='lead_9', color = 'firebrick')
    axes[3,1].set_title('Lead 9')
    axes[4,1].plot(time, lead_10, label='lead_10', color = 'dimgray')
    axes[4,1].set_title('Lead 10')
    axes[5,1].plot(time, lead_11, label='lead_11', color = 'crimson')
    axes[5,1].set_title('Lead 11')

    plt.tight_layout()
    plt.show()
