# I mean, thx and all, but....
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer, time

#import controller as controller
import event 
import pagemanager

import os.path 

import pprint 

appState = {
    'current_page': {
        # 'next_page': 'file://sample/8716.html'
        # 'next_page': 'file:' + os.path.join('.', 'sample', '8716.html')
        #'audio_source_url': 'file://sample/8716.html'
        'audio_source_url': 'file:sample/8716.html'
    }
}

# {'artist': 'TheNegativeInfluence',
#  'audio_file_url': '//mefimusic.s3.amazonaws.com/Down%20a%20Hole.mp3',
#  'audio_source_url': 'http://music.metafilter.com/8716/Down-a-Hole',
#  'list_title': '.Evaluation Hopper',
#!!! THIS IS NOT THE SAME IN 
#  'mp3_localfile': 'C:\\Users\\Bill\\Music\\MetaFilter\\.Evaluation '
#                   'Hopper\\TheNegativeInfluence - Down a Hole.mp3',
#  'newer': {'href': 'https://music.metafilter.com/8717/It-Dont-Matter-Whos-First-In-Line'},
#  'older': {'href': 'https://music.metafilter.com/8715/Manhattan-Skyline'},
#  'title': 'Down a Hole'}

def main():
    appState['current_page'] = pagemanager.get(appState['current_page']['audio_source_url'], provision_data = True, blocking = True)
    appState['next_page'] = pagemanager.get(appState['current_page']['newer']['href'])
    pprint.pprint(appState)
    exit()

    # Some things we need for metafodder:
    # +  artist
    # +  title
    #   list_name
    #   path

    # Other things:
    # #"published_parsed": entry.published_parsed,
    #        +    "audio_file_url": url,
    #        -    "audio_source_url": entry.link

    mixer.init()

    mixer.music.load('c:/Users/Bill/Music/MetaFilter/Chrismas is a swell time a hell time/Lentrohamsanin - Jingle Rock Bell.mp3')
    mixer.music.play(0)

    lastEvent = ''
    done = 0

    while not(done):
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

if __name__ == '__main__':
    main()            