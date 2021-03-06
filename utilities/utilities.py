import os
import sys
from tqdm import tqdm,tnrange
import time
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import shutil
from music21 import *
from utilities.constants import *


def organize_xml_files(path):
    
    numfolders = 0

    for directory in os.listdir(path):
        numfolders += 1
        try:
            if not os.listdir(os.path.join(path,directory)):
                os.rmdir(os.path.join(path,directory))
                numfolders -= 1
        except(NotADirectoryError):
            pass

    for subdir ,_ ,files in os.walk(path):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension == ".xml":
                file_path = os.path.join(subdir, file)
                file_dest = os.path.join(path, file)
                os.rename(file_path, file_dest)
                if not subdir == path:
                    #os.rmdir(subdir)
                    shutil.rmtree(subdir)
                    
########################################################################

def show_music21_settings():
    
    us = environment.UserSettings()
    
    #us.create()

    #configure.run()

    for key in sorted(us.keys()):
        try:
            tmp = us[key]
        except:
            tmp = "None"
        print("{0} - {1}".format(key,tmp))
        
########################################################################
        
def get_all_pitchclassdistribution_df(path, direction = "all", distance_th = 2, plots_dir = PLOTS_DIR):
    
    number_of_files = int(sum(1 for _ in os.listdir(path)))

    pitchclass_df = pd.DataFrame()
    
    for score,i in zip(os.listdir(path),tnrange(number_of_files-1)):
        
        _, extension = os.path.splitext(score)
        
        if extension == ".xml":
            
            s = converter.parse(os.path.join(path,score))
            #print("s:",s)
            
            classes,percentage = get_pitch_class_percentage(s, direction, distance_th, plots_dir)
            
            classes = [str(x) for x in classes]
            percentage = [[x] for x in percentage]
            
            tmp_df = pd.DataFrame(dict(zip(classes,percentage)))
            
            pitchclass_df = pd.concat([pitchclass_df,tmp_df],sort = True, ignore_index = True)
            
    return pitchclass_df

########################################################################

def get_pitch_class_percentage(score, direction, distance_th, plots_dir = PLOTS_DIR):
        #directions asc = ascendant, desc = descendant, all
        
        pitches = score.parts[0].pitches
        
        #print("pitches:", pitches)
        
        midi_pitches = select_vibrato_pitches_direction(pitches, direction, distance_th, plots_dir)
        
        count_pitch_classes = defaultdict(int)
        
        for note in midi_pitches:
            count_pitch_classes[int(note%12)] += 1
        
        pitch_classes = sorted(list(count_pitch_classes.keys()))
        data = []
        
        for c in pitch_classes:
            data.append(count_pitch_classes[c])
        
        data = 100*np.array(data)/sum(data)
        
        return pitch_classes, data

########################################################################

def select_vibrato_pitches_direction(pitches,direction,distance_th,plots_dir = PLOTS_DIR):
    
        if not direction in ["all","desc","asc"]:
            raise ValueError('Only all, desc, asc modes accepted')
        if distance_th<=0:
            raise ValueError('distance_th must be ≥1')

        tmp_plots_dir = os.path.join(plots_dir,direction)

        if not os.path.exists(tmp_plots_dir):
            os.mkdir(tmp_plots_dir)

        midi_pitches = [p.ps for p in pitches]

        if direction == "all":
            return midi_pitches

        midi_pitches = np.array(midi_pitches)

        #print("midi_pitches:", midi_pitches)

        difference = np.diff(midi_pitches)
        difference = np.clip(difference, a_min = -1, a_max = 1)

        #print("difference:", difference)

        state = "null"
        in_a_vibrato = False
        selection = []
        state_arr = [0 for _ in range(distance_th)]

        for i in range(distance_th,len(midi_pitches)-distance_th):
            
            in_a_vibrato = (difference[i] + difference[i-1] == 0)

            suma = sum(difference[(i-distance_th):(i+distance_th)])
            
            if (suma >= distance_th/2):
                state = "asc"
                if (in_a_vibrato): state_arr.append(1)
                else: state_arr.append(0)
            elif (suma <= -1*distance_th/2):
                state = "desc"
                if (in_a_vibrato): state_arr.append(-1)
                else: state_arr.append(0)
            elif abs(suma) <= 1:
                if (in_a_vibrato):
                    if state == "asc":
                        state_arr.append(1)
                    elif state == "desc":
                        state_arr.append(-1)
                else: state_arr.append(0)
            else:
                state = "null"
                state_arr.append(0)
                
            if state == "asc" and state == direction and in_a_vibrato:
                selection.append(midi_pitches[i])
            elif state == "desc" and state == direction and in_a_vibrato:
                selection.append(midi_pitches[i])

        for _ in range(distance_th):
            state_arr.append(0)
            
            #print(str(midi_pitches[i]) + "," + str(difference[i]) + " suma:" + str(suma) + "state:" + state)

        # Removing peaks and meloodic lines
        for i, state in enumerate(state_arr):
            
            #Checking if we have enough states to compute
            if ( i+4 < len(state_arr) ):
                
                # Reference state
                ref_state = state_arr[i+1]
                
                # 3 together
                if (
                    (state_arr[i] != ref_state) &
                    (state_arr[i+1] == ref_state) &
                    (state_arr[i+2] == ref_state) &
                    (state_arr[i+3] == ref_state) &
                    (state_arr[i+4] != ref_state)
                ):
                    state_arr[i+1] = 0
                    state_arr[i+2] = 0
                    state_arr[i+3] = 0
            
            #Checking if we have enough states to compute
            if ( i+3 < len(state_arr) ):
                
                # 2 together
                if (
                    (state_arr[i] != ref_state) &
                    (state_arr[i+1] == ref_state) &
                    (state_arr[i+2] == ref_state) &
                    (state_arr[i+3] != ref_state)
                ):
                    state_arr[i+1] = 0
                    state_arr[i+2] = 0
            
            #Checking if we have enough states to compute
            if ( i+2 < len(state_arr) ):
                
                # Single
                if (
                    (state_arr[i] != ref_state) &
                    (state_arr[i+1] == ref_state) &
                    (state_arr[i+2] != ref_state)
                ):
                    state_arr[i+1] = 0
        
        num = int(sum(1 for _ in os.listdir(tmp_plots_dir)))

        plt.figure(figsize = (10,8))
        state_arr = (np.max(midi_pitches)-np.mean(midi_pitches))*np.array(state_arr)+np.mean(midi_pitches)
        plt.scatter(np.arange(100),state_arr[:100], color = 'b')
        plt.plot(midi_pitches[:100], color = 'r')
        plotname = "{0}/test_{1}{2}".format(tmp_plots_dir,num,".png")
        plt.savefig(plotname, dpi = 300)
        plt.close()

        return selection
    
########################################################################

def add_missing_columns(df):
    missing_columns = list(set(np.arange(12)) - set([int(item) for item in list(df)]))
    sLength = len(df[list(df)[0]])
    for col in missing_columns:
        df[col] = pd.Series(np.zeros(sLength).fill(np.nan), index=df.index)
    return df   

########################################################################

def sort_df_columns_int(df):
    df = df.transpose()
    df.index = df.index.astype(int)
    df = df.sort_index().transpose().replace(np.nan, 0)
    return df