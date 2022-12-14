from annotateTest import *
import pandas as pd
import matplotlib.pyplot as plt
import neurokit2 as nk
plt.rcParams.update({'font.size':12})

#############################################################################
## Turn 12 LEAD ECG plot on/off

plots_on = False

##############################################################################

### ECG Numbers for Each Arrythmia ###
## Good
goodAV = [19,69,78,86,92]
goodRB = [19,242,290,331,416,627,791]
goodLB = [59,92,100,142,218,523]
goodSB = [41,69,99,189]
goodAF = [121,260,349,416]
goodST = [24,34,70,109,149]

## BAD
badAV = [58,759,791]
badRB = [149,357]
badLB = [280,342]
badSB = [152,439,627]
badAF = [356]
badST = [122,523,682]

##############################################################################

patient_num = goodAV+goodRB+goodLB+goodSB+goodAF+goodST+badAV+badRB+badLB+badSB+badAF+badST
#patient_num=[556,99]

##############################################################################




for i in patient_num:
    ### Set up patient data
    patient_ecg = 'Patient_ECGs/patient' + str(i) + '.csv'
    data = pd.read_csv(patient_ecg)

    ### Extract correct diagnosis
    gold_standard = 'Our_Files/gold_standard.csv'
    correct_diagnosis = pd.read_csv(gold_standard)
    correct_diagnosis = correct_diagnosis.T
    gold_standard_result = correct_diagnosis[i - 1]
    diagnosis_list = list(gold_standard_result)
    print(diagnosis_list)



    ### Extract Model Output of Probabilities
    classifications = 'Our_Files/ecg_output.csv'
    diagnosis = pd.read_csv(classifications)
    diagnosis = diagnosis.T
    patient_prob = diagnosis[i]
    probs_list = list(patient_prob)

    for x in range(6):
        if (probs_list[x] > 0.15):
            probs_list[x] = 1
        else:
            probs_list[x] = 0

    print(probs_list)
    if (probs_list != diagnosis_list):
        print("patient #" + str(i+1))
    ### Test for Arrythmias and Visualize
    print("patient #" + str(i+1))
    arrythmias_to_test(probs_list, diagnosis_list, data, i)



    

    if plots_on == True:

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
        plt.show(block=False)


### Controls how ECGs are cylced through

    #input()
    plt.pause(5)
    plt.close('all')

##############################################################################