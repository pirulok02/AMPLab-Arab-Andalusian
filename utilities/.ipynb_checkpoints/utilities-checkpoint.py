import os
import sys
from utilities.constants import *
from music21 import *
from collections import defaultdict
import numpy as np


def organize_xml_files():
    
    numfolders = 0

    for directory in os.listdir(SCORES_DIR):
        numfolders += 1
        try:
            if not os.listdir(os.path.join(SCORES_DIR,directory)):
                os.rmdir(os.path.join(SCORES_DIR,directory))
                numfolders -= 1
        except(NotADirectoryError):
            pass

    for subdir ,_ ,files in os.walk(SCORES_DIR):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension == ".xml":
                file_path = os.path.join(subdir, file)
                file_dest = os.path.join(SCORES_DIR, file)
                os.rename(file_path, file_dest)
                if not subdir == SCORES_DIR:
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