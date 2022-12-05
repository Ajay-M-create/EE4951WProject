# Run this as "python annotate.py"

import math as m
import matplotlib.pyplot as plt
import neurokit2 as nk
import pandas as pd
plt.rcParams.update({'font.size':12})


### Find the heart rate of any ECG
def find_heart_rate(data):
    avg = data[1] - data[0]
    if (len(data) < 3):
        return avg

    for x in range(1,len(data) - 1):
        newDist = data[x + 1] - data[x]
        avg = (avg + newDist)/2
    
    ans = (1/avg)*(400)*(60)
    return ans


### Calculates the PR interval
def PR_interval(Ploc, Rloc):
    dist = [0] * (len(Ploc) - 1)

    for i in range(0,len(Ploc) - 1):
        dist[i] = Rloc[i + 1] - Ploc[i + 1]

    return (sum(dist)/(len(Ploc) - 1))/400


### Calculate the TP interval
def TP_interval(Tloc, Ploc):
    dist = [0] * (len(Ploc) - 1)

    for i in range(0,len(Ploc) - 1):
        dist[i] = Ploc[i + 1] - Tloc[i]

    return (sum(dist)/(len(Ploc) - 1))/400


### Calculate the QRS interval
def QRSinterval(Q,S):
    QRS = [0] * (len(Q) - 1)
    # Start at second QRS complex because the first one can be messy
    for i in range(0,len(Q) - 1):
        if (m.isnan(S[i+1]) or m.isnan(Q[i+1])):
            pass
        else:
            QRS[i] = S[i+1] - Q[i+1]

    return (sum(QRS)/(len(Q)-1)/400)+0.04

### Stores the RR intervals for other calculations
def store_RR_interval(data):
    intervals = [0] *len(data)
    for x in range(1,len(data) - 1):
        intervals[x] = data[x + 1] - data[x]

    return intervals




### Annotae Sinus Tac
def visualizeSinusTac(data, R_loc, ECG, fig, axTac, message):
    R_locations = R_loc["ECG_R_Peaks"]
    LeadTwo = ECG.iloc[:,1][0:4000]
    time = list(range(0, len(LeadTwo)))
    graphicTac = axTac.plot(time, LeadTwo, label='DII', color = 'orange')
    axTac.set_title("Sinus Tachycardia")
    axTac.set_ylim(-1.5,1.5)

    if (message == ""):
        axTac.annotate(message + "Heart Rate is\ntoo fast: "+str(round(data,2))+"BPM", xy=(R_locations[1],0.5), xycoords='data', xytext=(R_locations[2], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTac.axvspan(R_locations[1],R_locations[2], facecolor='g', alpha=0.5)
    else:
        axTac.annotate(message + "Heart Rate is\nnot too fast", xy=(R_locations[1],0.5), xycoords='data', xytext=(R_locations[2], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTac.axvspan(R_locations[1],R_locations[2], facecolor='r', alpha=0.5)

    axTac.set_xlim(R_locations[1]-500,R_locations[2]+500)
    

### Annotate Sinus Brac
def visualizeSinusBrac(data, R_loc, ECG, fig, axBrac, message):
    R_locations = R_loc["ECG_R_Peaks"]
    LeadTwo = ECG.iloc[:,1][0:4000]
    time = list(range(0, len(LeadTwo)))
    graphicBrac = axBrac.plot(time, LeadTwo, label='DII', color = 'orange')
    axBrac.set_title("Sinus Bradycardia")
    axBrac.set_ylim(-1.5,1.5)

    if (message == ""):
        axBrac.annotate(message + "Heart Rate is\ntoo slow: "+str(round(data,2))+" BPM", xy=(R_locations[1],0.25), xycoords='data', xytext=(R_locations[2], 0.25), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axBrac.axvspan(R_locations[1],R_locations[2], facecolor='g', alpha=0.5)
    else:
        axBrac.annotate(message + "Heart Rate is\nnot too slow", xy=(R_locations[1],0.25), xycoords='data', xytext=(R_locations[2], 0.25), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axBrac.axvspan(R_locations[1],R_locations[2], facecolor='r', alpha=0.5)

    axBrac.set_xlim(R_locations[1]-500,R_locations[2]+500)


### Annoate AV Block
def visualizeAVBlock(data, R_loc, P_loc, ECG, fig, axAV, message):
    print(R_loc)
    print(P_loc)
    LeadTwo = ECG.iloc[:,7][0:4000]
    time = list(range(0, len(LeadTwo)))
    graphic = axAV.plot(time, LeadTwo, label='V3', color = 'orange')
    axAV.set_title("AV Block")

    if (message == ""):
        axAV.annotate(message + "PR Interval is\ntoo long: "+str(round(data,2))+" sec", xy=(P_loc[1],0), xycoords='data', xytext=(R_loc[1], 0), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axAV.axvspan(P_loc[1], R_loc[1], facecolor='g', alpha=0.5)
    else:
        axAV.annotate(message + "PR Interval is\ntoo long: "+str(round(data,2))+" sec", xy=(P_loc[1],0), xycoords='data', xytext=(R_loc[1], 0), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axAV.axvspan(P_loc[1], R_loc[1], facecolor='r', alpha=0.5)

    axAV.set_xlim(P_loc[1]-500,R_loc[1]+500)

def visualizeBBB(data, Q, S, ECG, fig, axQRS, message, LR):
    Lead6 = ECG.iloc[:,10][0:4000]
    time = list(range(0, len(Lead6)))
    graphic = axQRS.plot(time, Lead6, label='V1', color = 'orange')
    if (LR == "left"):
        axQRS.set_title("Left Branch Bundle Block")
    else:
        axQRS.set_title("Right Branch Bundle Block")
    
    if (message == ""):
        axQRS.annotate(message + "QRS Interval is\ntoo long: "+str(round(data+0.1,2))+" sec", xy=(Q[2]-25,Lead6[Q[2]]/2), xycoords='data', xytext=(S[2]+25, Lead6[Q[2]]/2), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axQRS.axvspan(Q[2]-25,S[2]+25, facecolor='g', alpha=0.5)
    elif (message == "Model missed LBBB\n"):
        axQRS.annotate(message + "QRS Interval is greater than 0.12 sec", xy=(Q[2]-25,Lead6[Q[2]]/2), xycoords='data', xytext=(S[2]+25, Lead6[Q[2]]/2), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axQRS.axvspan(Q[2]-25,S[2]+25, facecolor='r', alpha=0.5)
    else:
        axQRS.annotate(message + "QRS Interval is: "+str(round(data,3))+" sec", xy=(Q[2]-25,Lead6[Q[2]]/2), xycoords='data', xytext=(S[2]+25, Lead6[Q[2]]/2), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axQRS.axvspan(Q[2]-25,S[2]+25, facecolor='r', alpha=0.5)
    
    axQRS.set_xlim(1000,2000)
    print(Q)
    print(S)



### Annotate Atrial Fib
def visualizeAtrFib(data, P, T, R, ECG, fig, axTP, message):
    LeadTwo = ECG.iloc[:,1][0:4000]
    time = list(range(0, len(LeadTwo)))
    graphic = axTP.plot(time, LeadTwo, label='V1', color = 'orange')
    axTP.set_title("Atrial Fibrillation")

    if (message == ""):
        axTP.annotate("", xy=(R[1],0.5), xycoords='data', xytext=(R[2], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.annotate("", xy=(R[2],0.5), xycoords='data', xytext=(R[3], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.annotate("", xy=(R[3],0.5), xycoords='data', xytext=(R[4], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.annotate("RR distances are inconsistent", xy=(R[4],0.5), xycoords='data', xytext=(R[5], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.annotate(message + "TP Interval is spiky", xy=(T[2]-25,0), xycoords='data', xytext=(P[2]+25, 0), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.axvspan(T[2]-25,P[2]+25, facecolor='g', alpha=0.5)
        axTP.axvspan(R[3], R[5], facecolor='g', alpha=0.5)
    else:
        axTP.annotate("", xy=(R[1],0.5), xycoords='data', xytext=(R[2], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.annotate("", xy=(R[2],0.5), xycoords='data', xytext=(R[3], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.annotate("", xy=(R[3],0.5), xycoords='data', xytext=(R[4], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.annotate("Model missed Inconsistent\nRR peak distances", xy=(R[4],0.5), xycoords='data', xytext=(R[5], 0.5), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))
        axTP.annotate("Model missed the noise\n indicative of A Fib", xy=(T[2]-25,-0.2), xycoords='data', xytext=(P[2]+25, -0.2), textcoords='data', arrowprops=dict(arrowstyle="|-|,widthA=2.0,widthB=2.0", connectionstyle="arc3"))    
        axTP.axvspan(T[2]-25,P[2]+25, facecolor='r', alpha=0.5)
        axTP.axvspan(R[3], R[5], facecolor='r', alpha=0.5)

    axTP.set_xlim(300,3000)
    print(T)
    print(P)


### First function to be called from main.py
### Cycles through each of the predictions and annoates them correct or incorrect
def arrythmias_to_test(dataModel, dataGold, ECG, num):

    fig = plt.figure(figsize=(25.6,16.0), dpi=100)

    ax = fig.subplots(max(sum(dataModel),sum(dataGold),2))
    i = 0

    ### AV Block
    if (dataGold[0] != dataModel[0]):
        PR_interval, R_Loc, P_Loc = av_block(ECG)
        print("Incorrect PR Interval: ", str(PR_interval))
        message = ""
        if (dataGold[0] == 1):
            message = "Model missed AV Block\n"
            print("Model underpredicted")
        elif (dataGold[0] == 0):
            message = "Model incorrectly predicted AV Block\n"
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
            message = "Model missed RBBB\n"
            print("Model underpredicted RBBB")
        elif (dataGold[1] == 0):
            message = "Model incorrectly predicted RBBB\n"
            print("Model over predicted RBBB")
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message, "right")
        i += 1
    elif (dataGold[1] == 1):
        message = ""
        QRS_dist, Q, S = find_QRS_dist(ECG)
        print("Correct QRS Interval for RBBB")
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message, "right" )
        i += 1




    ### LBBB
    if (dataGold[2] != dataModel[2]):
        QRS_dist, Q, S = find_QRS_dist(ECG)
        print("incorrect QRS interval for LBBB")
        message = ""
        if (dataGold[2] == 1):
            message = "Model missed LBBB\n"
            print("Model underpredicted LBBB")
        elif (dataGold[2] == 0):
            message = "Model incorrectly predicted LBBB\n"
            print("Model over predicted LBBB")
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message, "left")
        i += 1
    elif (dataGold[2] == 1):
        message = ""
        QRS_dist, Q, S = find_QRS_dist(ECG)
        print("Correct QRS Interval for LBBB")
        visualizeBBB(QRS_dist, Q, S, ECG, fig, ax[i], message, "left")
        i += 1


    ### Sinus Brac
    if (dataGold[3] != dataModel[3]):
        rate, R_loc = sinus_brac(ECG)
        print("Incorrect sinus brac: " + str(rate))
        message = ""
        if (dataGold[3] == 1):
            message = "Model missed Sinus\nBradycardia\n"
            print("Model under predicted the heart rate for sinus brac")
        elif (dataGold[3] == 0):
            message = "Model incorrectly predicted\nSinus Bracycardia\n"
            print("Model over predicted the heart rate for sinus brac")
        visualizeSinusBrac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1
    elif (dataGold[3] == 1):
        rate, R_loc = sinus_brac(ECG)
        print("Correct sinus brac: " + str(rate))
        message = ""
        visualizeSinusBrac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1



    ### A-Fib
    if (dataGold[4] != dataModel[4]):
        TP_interval, T_loc, P_loc = atrial_fib(ECG)
        rate, R_loc = sinus_brac(ECG)
        if (dataGold[4] == 1):
            message = "Model missed afib"
            
        elif (dataGold[4] == 0):
             message = "Model incorrectly predicted afib"
        print(message)
        visualizeAtrFib(TP_interval, T_loc, P_loc, R_loc["ECG_R_Peaks"], ECG, fig, ax[i], message)
    elif (dataGold[4] == 1):
        message = ""
        TP_interval, T_loc, P_loc = atrial_fib(ECG)
        print("Correct TP Interval: ", str(TP_interval))
        rate, R_loc = sinus_brac(ECG)
        visualizeAtrFib(TP_interval, T_loc, P_loc, R_loc["ECG_R_Peaks"], ECG, fig, ax[i], message)
        i += 1
        

    ### Sinus Tac
    if (dataGold[5] != dataModel[5]):
        rate, R_loc = sinus_tac(ECG)
        print("Incorrect sinus tac: " + str(rate))
        message = ""
        if (dataGold[5] == 1):
            message = "Model missed Sinus Tacycardia\n"
            print("Model under predicted the heart rate for sinus tac")
        elif (dataGold[5] == 0):
            message = "Model incorrectly predicted\nSinus Tacycardia\n"
            print("Model over predicted the heart rate for sinus tac")
        visualizeSinusTac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1
    elif (dataGold[5] == 1):
        rate, R_loc = sinus_tac(ECG)
        print("Correct sinus tac: " + str(rate))
        message = ""
        visualizeSinusTac(rate, R_loc, ECG, fig, ax[i], message)
        i += 1


    if (max(sum(dataModel),sum(dataGold)) == 1):
        ax[1].set_axis_off()


    
    ### If using code to run ECG, un comment the line below to see annoations
    plt.show(block=False)
    #plt.savefig(str(num)+'.png', bbox_inches='tight')


### find QRS interval for use with LBBB nad RBBB
def find_QRS_dist(ECG):
    clean_ecg = ECG.iloc[:,10][0:4000]
    # Extract Q and S locations
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    PQST_locations, PQST = nk.ecg_delineate(clean_ecg, R_info_dict, sampling_rate=400, method='dwt')
    Q_locations = PQST['ECG_Q_Peaks']  
    S_locations = PQST['ECG_S_Peaks']
    QRS_dist = QRSinterval(Q_locations, S_locations)  
    print("QRS: " + str(QRS_dist))
    return QRS_dist, Q_locations, S_locations


### Determine Sinus Brac
def sinus_brac(ECG):
    # Extract R-peaks locations
    clean_ecg = ECG.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    rate = find_heart_rate(R_info_dict['ECG_R_Peaks'])
    if (rate < 60):
        return rate, R_info_dict
    else:
        return rate, R_info_dict

### Deteermine Sinus Tac
def sinus_tac(ECG):
    # Extract R-peaks locations
    clean_ecg = ECG.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    rate = find_heart_rate(R_info_dict['ECG_R_Peaks'])
    if (rate > 100):
        return rate, R_info_dict
    else:
        return rate, R_info_dict

### Determine AV block
def av_block(ECG):
    # Extract R-peaks locations
    clean_ecg = ECG.iloc[:,7][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    # Extract P-peak locations
    PQST_locations, PQST = nk.ecg_delineate(clean_ecg, R_info_dict, sampling_rate=400, method='dwt')
    P_locations = PQST['ECG_P_Peaks']
    result = PR_interval(P_locations, R_info_dict['ECG_R_Peaks'])
    result = round(result, 1)
    if (result >= 0.2):
        return result, R_info_dict["ECG_R_Peaks"], P_locations
    else:
        return result, R_info_dict["ECG_R_Peaks"], P_locations


### Determine Atrial fib
def atrial_fib(ECG):
    # Extract R-peaks locations
    clean_ecg = ECG.iloc[:,1][0:4000]
    R_locations, R_info_dict = nk.ecg_peaks(clean_ecg, sampling_rate=400)
    # Extract P-peak locations
    PQST_locations, PQST = nk.ecg_delineate(clean_ecg, R_info_dict, sampling_rate=400, method='dwt')
    P_locations = PQST['ECG_P_Peaks']
    T_locations = PQST['ECG_T_Peaks']
    result = TP_interval(T_locations, P_locations)
    result = round(result, 1)
    if (result >= 0.2):
        return result, T_locations, P_locations
    else:
        return result, T_locations, P_locations
