from music21 import *

def printsettings(us):
    for key in sorted(us.keys()):
        try:
            tmp = us[key]
        except:
            tmp = "None"
        print("{0} - {1}".format(key,tmp))


us = environment.UserSettings()
#us.create()

printsettings(us)

#configure.run()

printsettings(us)
#environment.set('musicxmlPath','/usr/bin/mscore')
#environment.set('showFormat','lilypond')
#environment.set('musescoreDirectPNGPath','/usr/bin/mscore')
#environment.set('lilypondPath','/usr/bin/lilypond')
