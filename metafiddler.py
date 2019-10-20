

from pygame import mixer, time
import metafiddler.controller as controller
import metafiddler.event as event
import metafiddler.pagemanager

import os.path 

appState = {
    #'next_page': 'file://sample/8716.html'
    'next_page': 'file:8716.html'
#    'next_page': 'file:' + os.path.join('.', 'sample', '8716.html')
}

page = metafiddler.pagemanager.get(appState['next_page'])
print(page)

exit()

mixer.init()

mixer.music.load('c:/Users/Bill/Music/MetaFilter/Chrismas is a swell time a hell time/Lentrohamsanin - Jingle Rock Bell.mp3')
mixer.music.play(0)

lastEvent = ''
while mixer.music.get_busy():
    # This event stacking makes it seem like we're not going to deal
    # with +1 events and, um, yes, wait for the next poll and 
    # pop them off your stack or something.
    e = controller.poll()

    # Debounce event
    if lastEvent != e:
        print(e)
        if e == event.STOP:
            print("-> Stop!")
            mixer.music.stop()
        #elif event == event.PLAY:
            # Some higgedy about already playing
        lastEvent = e

    #time.Clock().tick(.25)