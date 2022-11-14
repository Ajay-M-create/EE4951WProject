# Run this as "python annotate.py"

import math as m

import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np
import pandas as pd
from ecgdetectors import Detectors


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

    for i in range(0,len(Ploc) - 1):
        #print("distance added: " + str(dist))
        dist[i] = Rloc[i + 1] - Ploc[i + 1]

    return (sum(dist)/(len(Ploc) - 1))/400


#in progress - used for AtrFib
def TP_interval(Tloc, Ploc):
    dist = [0] * (len(Ploc) - 1)

    for i in range(0,len(Ploc) - 1):
        #print("distance added: " + str(dist))
        dist[i] = Ploc[i + 1] - Tloc[i]

    return (sum(dist)/(len(Ploc) - 1))/400


def QRSinterval(Q,S):
    QRS = [0] * (len(Q) - 1)
    # Start at second QRS complex because the first one can be messy
    for i in range(0,len(Q) - 1):
        if (m.isnan(S[i+1]) or m.isnan(Q[i+1])):
            pass
        else:
            QRS[i] = S[i+1] - Q[i+1]

    return (sum(QRS)/(len(Q)-1)/400)+0.04

def store_RR_interval(data):
    intervals = [0] *len(data)
    for x in range(1,len(data) - 1):
        intervals[x] = data[x + 1] - data[x]

    return intervals





def visualizeSinusTac(data, R_loc, ECG, fig, axTac, message):
    R_locations = R_loc["ECG_R_Peaks"]
    LeadTwo = ECG.iloc[:,1][0:4000]
    time = list(range(0, len(LeadTwo)))
    #fig = plt.figure()
    #axTac = fig.add_subplot()
    graphicTac = axTac.plot(time, LeadTwo, label='DII', color = 'orange')
    axTac.annotate(message + "Heart Rate: "+str(round(data,2))+"BPM", xy=(R_locations[1],0.5), xycoords='data', xytext=(R_locations[2], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
    axTac.set_ylim(-1.5,1.5)
    axTac.set_xlim(R_locations[1]-500,R_locations[2]+500)
    #plt.show()
    

def visualizeSinusBrac(data, R_loc, ECG, fig, axBrac, message):
    R_locations = R_loc["ECG_R_Peaks"]
    LeadTwo = ECG.iloc[:,1][0:4000]
    time = list(range(0, len(LeadTwo)))
    #fig = plt.figure()
    #axBrac = fig.add_subplot()
    graphicBrac = axBrac.plot(time, LeadTwo, label='DII', color = 'orange')
    axBrac.annotate(message + "Heart Rate: "+str(round(data,2))+" BPM", xy=(R_locations[1],1.0), xycoords='data', xytext=(R_locations[2], 1.0), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
    axBrac.set_ylim(-1.5,1.5)
    axBrac.set_xlim(R_locations[1]-500,R_locations[2]+500)
    #plt.show()

def visualizeAVBlock(data, R_loc, P_loc, ECG, fig, axAV, message):
    print(R_loc)
    print(P_loc)
    LeadTwo = ECG.iloc[:,7][0:4000]
    time = list(range(0, len(LeadTwo)))
    #fig = plt.figure()
    #ax = fig.add_subplot()
    graphic = axAV.plot(time, LeadTwo, label='V3', color = 'orange')
    axAV.annotate(message + "PR Interval: "+str(round(data,2))+" sec", xy=(P_loc[1],0), xycoords='data', xytext=(R_loc[1], 0), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
    #axAV.set_ylim(-1.5,1.5)
    axAV.set_xlim(P_loc[1]-500,R_loc[1]+500)
    #plt.show()

def visualizeBBB(data, Q, S, ECG, fig, axQRS, message):
    Lead6 = ECG.iloc[:,10][0:4000]
    time = list(range(0, len(Lead6)))
    graphic = axQRS.plot(time, Lead6, label='V1', color = 'orange')
    axQRS.annotate(message + "QRS Interval: "+str(round(data,2))+" sec", xy=(Q[2]-25,0), xycoords='data', xytext=(S[2]+25, 0), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
    #axQRS.set_ylim(-1.5,1.5)
    axQRS.set_xlim(400,3000)
    print(Q)
    print(S)

#still fixing
def visualizeAtrFib(data, P, T, ECG, fig, axTP, message):
    LeadTwo = ECG.iloc[:,1][0:4000]
    time = list(range(0, len(LeadTwo)))
    graphic = axTP.plot(time, LeadTwo, label='V1', color = 'orange')
    axTP.annotate(message + "TP Interval is spiky, RR distances are inconsistent", xy=(T[2]-25,0), xycoords='data', xytext=(P[2]+25, 0), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
    #axQRS.set_ylim(-1.5,1.5)
    axTP.set_xlim(400,3000)
    print(T)
    print(P)


'''
This function needs to be complete. It takes in the gold standard results, and then confirm if they
exist, and returns whether or not it found them
'''
def arrythmias_to_test(dataModel, dataGold, ECG):
    fig = plt.figure()
    ax = fig.subplots(sum(dataModel))
    i = 0
    """
    ### AV Block
    if (dataModel[0] == 1 and dataGold[0] == 1):
        PR_interval, R_Loc, P_Loc = av_block(ECG)
        visualizeAVBlock(PR_interval, R_Loc, P_Loc, ECG, fig, ax[i])
        i += 1
    else:
        incorrect[0] = dataGold[0]

   
    ### Still working on all of this
    ### AV Block
    if (dataGold[0] == 1):
        PR_interval, R_Loc, P_Loc = av_block(ECG)
        print("PR Interval: ", str(PR_interval))
        if (dataModel[0] != 1):
            message = "Model missed the PR Interval\n"
            print("AV Block incorrect")
        else:
            message = ""
            print("AV Block Correct")
        visualizeAVBlock(PR_interval, R_Loc, P_Loc, ECG, fig, ax[i], message)
        i += 1
    """
    ### AV Block
    if (dataGold[0] != dataModel[0]):
        PR_interval, R_Loc, P_Loc = av_block(ECG)
        print("Incorrect PR Interval: ", str(PR_interval))
        message = ""
        if (dataGold[0] == 1):
            message = "Model underpredicted the PR Interval\n"
            print("Model underpredicted")
        elif (dataGold[0] == 0):
            message = "Model Over-predicted the PR Interval\n"
            print("Model Over-predicted")
        visualizeAVBlock(PR_interval, R_Loc, P_Loc, ECG, fig, ax[i], message)
        i += 1
    elif (dataGold[0] == 1):
        message = ""
        PR_interval, R_Loc, P_Loc = av_block(ECG)
        print("Correct PR Interval: ", str(PR_interval))
        visualizeAVBlock(PR_interval, R_Loc, P_Loc, ECG, fig, ax[i], message)
        i += 1



    ### RBBB
    if (dataGold[1] != dataModel[1]):
        QRS_dist, Q, S = find_QRS_dist(ECG)
        print("incorrect QRS interval for RBBB")
        message = ""
        if (dataGold[1] == 1):
            message = "Model underpredicted the QRS interval\n"
            print("Model underpredicted RBBB")
        elif (dataGold[1] == 0):
            message = "Model over predicted the QRS interval\n"
            print("Model over predicted RBBB")
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message)
        i += 1
    elif (dataGold[1] == 1):
        message = ""
        QRS_dist, Q, S = find_QRS_dist(ECG)
        print("Correct QRS Interval for RBBB")
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message)
        i += 1



    '''
    ### RBBB
    if (dataGold[1] == 1):
        QRS_dist, Q, S = find_QRS_dist(ECG)
        if (dataModel[1] != 1):
            message = "Model missed the QRS Complex\n"
            print("RBBB incorrect")
        else:
            message = ""
            print("RBBB Correct")
            ax[i].annotate("M wave on V1 lead", xy=(Q[2]-45,0.5), xycoords='data', xytext=(S[2]+45, 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i])
        i += 1

    
    ### RBBB
    if (dataModel[1] == 1 and dataGold[1] == 1): 
        visualizeSinusTac(rate, R_loc, ECG, fig, ax[i])
        #m, w = findMorW(ECG)
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i])
        ax[i].annotate("M wave on V1 lead", xy=(Q[2]-45,0.5), xycoords='data', xytext=(S[2]+45, 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        i += 1
    else:
        incorrect[1] = dataGold[1]
    '''

    ### LBBB
    if (dataGold[2] != dataModel[2]):
        QRS_dist, Q, S = find_QRS_dist(ECG)
        print("incorrect QRS interval for LBBB")
        message = ""
        if (dataGold[2] == 1):
            message = "Model underpredicted the QRS interval\n"
            print("Model underpredicted LBBB")
        elif (dataGold[2] == 0):
            message = "Model over predicted the QRS interval\n"
            print("Model over predicted LBBB")
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message)
        i += 1
    elif (dataGold[2] == 1):
        message = ""
        QRS_dist, Q, S = find_QRS_dist(ECG)
        print("Correct QRS Interval for LBBB")
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message)
        i += 1



    """

    ### LBBB
    if (dataGold[2] == 1):
        QRS_dist, Q, S = find_QRS_dist(ECG)
        if (dataModel[2] != 1):
            message1 = "Model missed the QRS Complex\n"
            print("LBBB incorrect")
        else:
            message1 = ""
            print("LBBB Correct")
            ax[i].annotate("W wave on V1 lead", xy=(Q[2]-45,0.5), xycoords='data', xytext=(S[2]+45, 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))

        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message1)
        i += 1
    """
    '''
    ### LBBB    
    if (dataModel[2] == 1 and dataGold[2] == 1):
        QRS_dist, Q, S = find_QRS_dist(ECG)
        #m, w = findMorW(ECG)
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i])
        ax[i].annotate("W wave on V1 lead", xy=(Q[2]-45,0.5), xycoords='data', xytext=(S[2]+45, 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        i += 1
    else:
        incorrect[2] = dataGold[2]
    '''
    ### Sinus Brac
    if (dataGold[3] != dataModel[3]):
        rate, R_loc = sinus_brac(ECG)
        print("Incorrect sinus brac: " + str(rate))
        message = ""
        if (dataGold[3] == 1):
            message = "Model under predicted the heart rate\n"
            print("Model under predicted the heart rate for sinus brac")
        elif (dataGold[3] == 0):
            message = "Model over predicted the hear rate\n"
            print("Model over predicted the heart rate for sinus brac")
        visualizeSinusBrac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1
    elif (dataGold[3] == 1):
        rate, R_loc = sinus_brac(ECG)
        print("Correct sinus brac: " + str(rate))
        message = ""
        visualizeSinusBrac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1

    '''

    ### Sinus Brac     
    if (dataModel[3] == 1 and dataGold[3] == 1):
        rate, R_loc = sinus_brac(ECG)
        print("sinus brac: " + str(rate))
        visualizeSinusBrac(rate, R_loc, ECG, fig, ax[i])
        i += 1
        print(store_RR_interval(R_loc['ECG_R_Peaks']))
    else:
        pass

    '''

    ### A-Fib
    if (dataGold[4] != dataModel[4]):
        if (dataGold[4] == 1):
            print("Model missed the afib")
        elif (dataGold[4] == 0):
            print("Model incorrectly predicted afib")
    elif (dataGold[4] == 1):
        message = ""
        TP_interval, T_loc, P_loc = atrial_fib(ECG)
        print("Correct TP Interval: ", str(TP_interval))
        visualizeAtrFib(TP_interval, T_loc, P_loc, ECG, fig, ax[i], message)
        i += 1
        
    '''
    ### Afib    
    if (dataModel[4] == 1 and dataGold[4] == 1):
        pass
    else:
        incorrect[4] = dataGold[4]
    ''' 
    '''  
    ### Sinus Tac  
    if (dataGold[5] == 1):
        rate, R_loc = sinus_tac(ECG)
        if (dataModel[5] != 1):
            message = "Model missed the Heart Rate\n"
            print("incorrect")
        else:
            message = ""
            print("correct")
        visualizeSinusTac(rate, R_loc, ECG, fig, ax[i], message)

        
    if (dataModel[5] == 1 and dataGold[5] == 1):
        rate, R_loc = sinus_tac(ECG)
        print("sinus tac: " + str(rate))   
        message = ""
        visualizeSinusTac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1  
    else:
        incorrect[5] = dataGold[5]
    '''
    ### Sinus Tac
    if (dataGold[5] != dataModel[5]):
        rate, R_loc = sinus_tac(ECG)
        print("Incorrect sinus tac: " + str(rate))
        message = ""
        if (dataGold[5] == 1):
            message = "Model under predicted the heart rate\n"
            print("Model under predicted the heart rate for sinus tac")
        elif (dataGold[5] == 0):
            message = "Model over predicted the hear rate\n"
            print("Model over predicted the heart rate for sinus tac")
        visualizeSinusTac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1
    elif (dataGold[5] == 1):
        rate, R_loc = sinus_tac(ECG)
        print("Correct sinus tac: " + str(rate))
        message = ""
        visualizeSinusTac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1


    #ax.set_xlim(0,2000)
    #ax.set_ylim(-2,2)

    plt.show(block=False) 

def find_QRS_dist(ECG):
    clean_ecg = ECG.iloc[:,10][0:4000]
    # Extract Q and S locations
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    PQST_locations, PQST = nk.ecg_delineate(clean_ecg, R_info_dict, sampling_rate=400, method='dwt')
    #plot = nk.events_plot([R_info_dict['ECG_R_Peaks'], PQST['ECG_P_Peaks'], PQST['ECG_Q_Peaks'], PQST['ECG_S_Peaks'], PQST['ECG_T_Peaks']], clean_ecg) 
    Q_locations = PQST['ECG_Q_Peaks']  
    S_locations = PQST['ECG_S_Peaks']
    QRS_dist = QRSinterval(Q_locations, S_locations)  
    print("QRS: " + str(QRS_dist))
    return QRS_dist, Q_locations, S_locations


def findMorW(ECG):

    return 0,0


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
    clean_ecg = ECG.iloc[:,7][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    # Extract P-peak locations
    PQST_locations, PQST = nk.ecg_delineate(clean_ecg, R_info_dict, sampling_rate=400, method='dwt')
    P_locations = PQST['ECG_P_Peaks']
    #print(R_info_dict['ECG_R_Peaks'])
    #print(P_locations)
    #plot = nk.events_plot([R_info_dict['ECG_R_Peaks'], P_locations], clean_ecg) 
    result = PR_interval(P_locations, R_info_dict['ECG_R_Peaks'])
    result = round(result, 1)
    if (result >= 0.2):
        return result, R_info_dict["ECG_R_Peaks"], P_locations
    else:
        return result, R_info_dict["ECG_R_Peaks"], P_locations


#still fixing, want to capture T to next P interval
def atrial_fib(ECG):
    # Extract R-peaks locations
    clean_ecg = ECG.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    # Extract P-peak locations
    PQST_locations, PQST = nk.ecg_delineate(clean_ecg, R_info_dict, sampling_rate=400, method='dwt')
    P_locations = PQST['ECG_P_Peaks']
    T_locations = PQST['ECT_T_Peaks']
    #print(R_info_dict['ECG_R_Peaks'])
    #print(P_locations)
    #plot = nk.events_plot([R_info_dict['ECG_R_Peaks'], P_locations, PQST['ECG_Q_Peaks'], PQST['ECG_S_Peaks'], PQST['ECG_T_Peaks']], clean_ecg) 
    result = TP_interval(T_locations, P_locations)
    result = round(result, 1)
    if (result >= 0.2):
        return result, T_locations, P_locations
    else:
        return result, T_locations, P_locations

