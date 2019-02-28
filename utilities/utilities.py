import os
import sys
from utilities.constants import *
from music21 import *
from collections import defaultdict
import numpy as np
import pandas as pd
from tqdm import tnrange


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
                    os.rmdir(subdir)
                    
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
        
def get_pitch_class_distribution(score):
    
    pitches = score.parts[0].pitches
    
    count_pitch_classes = defaultdict(int)
    
    for note in pitches:
        count_pitch_classes[int(note.ps%12)] += 1
        
    classes = sorted(list(count_pitch_classes.keys()))
    data = []
    for c in classes:
        data.append(count_pitch_classes[c])
    
    data = np.array(data)/sum(data)
    
    return classes, data

########################################################################

def get_pitchclassdistribution_df(path):
    
    number_of_files = int(sum(1 for _ in os.listdir(path)))

    pitchclass_df = pd.DataFrame()

    for score,i in zip(os.listdir(path),tnrange(number_of_files-1)):
        
        _, extension = os.path.splitext(score)
        
        if extension == ".xml":
            
            s = converter.parse(os.path.join(path,score))
            
            classes,percentage = get_pitch_class_distribution(s)
            
            classes = [str(x) for x in classes]
            percentage = [[100*x] for x in percentage]
            
            tmp_df = pd.DataFrame(dict(zip(classes,percentage)))
            pitchclass_df = pd.concat([pitchclass_df,tmp_df],sort = True, ignore_index = True)

    return pitchclass_df

