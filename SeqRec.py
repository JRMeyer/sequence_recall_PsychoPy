# -*- coding: utf-8 -*-
'''

USAGE: 
$ python SeqRec.py

DEPENDENCIES:
template.py

FILE STRUCTURE:

/
    SeqRec.py
    template.py
    SeqRec_master/
                  config.txt
                  audio_stims/
                              cond1_A/
                              cond1_B/
                              cond2_A/
                              cond2_B/
                              .
                              .
                              .

This script should be located in the same directory as the SeqRec_master/ dir
and template.py. The template.py script holds the patterns of how to create 
the sequences of audio stims to be played. These sequences come from Dupoux et
al (2001). If there is no pre-existing SeqRec_Master/ dir, running this script 
as shown in USAGE will configure a correct (but empty) file structure. The user
then must fill in those empty dirs with audio stims.

Filenames for the audio files should be of the form: 
    <condition>_<speaker>_<tokenNumber>_<A|B>.wav 
    e.g. kupo_peter_1_A.wav

'''

# from template.py
from template import templateList
# visual displays prompts, event gets keypresses, sound plays WAVs, core will
# shut us down
from psychopy import visual, event, sound, core, prefs
# For listing contents of a directory, manipulating filepaths
import os
# for regex
import re
# helps us ranomize stimuli presentation
import random
import sys
import numpy
# ast will convert string to python code for our config() function
import ast


class SeqRec():
    def __init__(self):
        # set our sound preferences
        prefs.general['audioLib'] = ['pygame']
        self.config()
        self.displayRes = [800,800]
        self.responses = []


    def config(self):
        if os.path.isfile('SeqRec_master/config.txt'):
            try:
                with open('SeqRec_master/config.txt') as f:
                    lines = f.readlines()

                for line in lines:
                    label,values = line.strip().split('\t')
                    if label == 'contrasts':
                        self.contrasts = ast.literal_eval(values)
                    elif label == 'speakers':
                        self.speakers = ast.literal_eval(values)
                    elif label == 'testCutOff':
                        self.testCutOff = float(ast.literal_eval(values)[0])
                    elif label == 'testISI':
                        self.testISI = float(ast.literal_eval(values)[0])
                    elif label == 'mainISI':
                        self.mainISI = float(ast.literal_eval(values)[0])
                    elif label == 'numForcedListens':
                        self.numForcedListens = int(ast.literal_eval(values)[0])
            except:
                print "ERROR: The config.txt file is not correctly formatted."
        else:
            self.create_config_file()

            
    def create_config_file(self):
        print '\n'

        print("Welcome to SeqRec! It seems you are a new user. We need\n"+
        "to complete a few steps in order to set up your experiment. You\n"+
        "will now be asked a series of questions, and that information\n"+
        "will be used to configure the experiment.\n"+
        "If you do this accurately (and do not delete or move the\n"+
        "config.txt file which will be produced), you should only need\n"+
        "to complete this process once.")

        print '\n'
        raw_input("Press any key to continue")
        print '\n'

        print("In the following questions, you will be asked for numbers\n"+
        "and labels of stimuli. You should enter the labels as they\n"+
        "appear in your filenames for the auditory stimuli. Any typos\n"+
        "will result in failure of the program to find your files. So be\n"+
        "careful to enter them correctly.")

        print '\n'
        raw_input("Press any key to continue")
        print '\n'

        print "Let's get started!"
        print '\n'
        core.wait(1)

        speakers=[]
        numSpeakers = raw_input("How many speakers are there for each"+
        " word?\n\tEnter a number here: ")
        print '\n'

        for i in range(1,int(numSpeakers)+1):
            speakers.append(raw_input("Enter speaker " +str(i)+
                        " here, as it appears in your audio filenames :  "))
            print '\n'

        contrasts=[]
        numContrasts = raw_input("How many sound contrasts do you have?\n"+
        "\tEnter a number here: ")
        print '\n'

        for i in range(1,int(numContrasts)+1):
            contrast=[]
            contrast.append(raw_input("Enter first word for contrast "
                                      +str(i)+ " here, as it appears in "+
                                       "the audio filenames :  "))
            print '\n'
            contrast.append(raw_input("Enter second word for "+
                                      "contrast " +str(i)+ " here, as it "+
                                       "appears in the audio filenames : "))
            print '\n'

            contrasts.append(contrast)

        testCutOff = [raw_input("How many correct responses in a row does\n"+
                        "the participant need to pass the testing phase?\n"+
                               "\tEnter a number here: ")]
        print '\n'

        testISI = [raw_input("What inter-stimulus interval (ISI) would\n"+
                        "you like for the testing phase?\n"+
                               "\tEnter a number here, in seconds: ")]
        print '\n'

        mainISI = [raw_input("What inter-stimulus interval (ISI) would\n"+
                        "you like between sounds within sequences during\n"+
                        "the main phase of the experiment?\n"+
                            "\tEnter a number here, in seconds: ")]
        print '\n'

        numForcedListens = [raw_input("How many stimuli would you like the\n"+
                        "participant to be forced to hear at the beginning of\n"+
                        "the experiment?\n"+
                            "\tEnter an even number here: ")]
        print '\n'

        configFile = open('SeqRec_master/config.txt', 'w')
        print >> configFile, 'speakers\t' + str(speakers)
        print >> configFile, 'contrasts\t' + str(contrasts)
        print >> configFile, 'testCutOff\t' + str(testCutOff)
        print >> configFile, 'testISI\t' + str(testISI)
        print >> configFile, 'mainISI\t' + str(mainISI)
        print >> configFile, 'numForcedListens\t' + str(numForcedListens)

        print "Configuration complete!\n"
        print "You may restart the experiment now.\n"
        print "Enjoy!\n"

        sys.exit()
                    

        
    def check_dir(self):
        # if the dir SeqRec_master/ doesn't exist, create it!
        if not os.path.exists("SeqRec_master/audio_stims"):
            # loop through the contrasts provided
            for contrast in self.contrasts:
                # make subfolders for the two words of contrast (A and B)
                os.makedirs("SeqRec_master/audio_stims/" + contrast[0] + "_A/")
                os.makedirs("SeqRec_master/audio_stims/" + contrast[1] + "_B/")
                
            # Tell the experimenter to put the audio files in folders
            self.display_prompt("ERROR: Put audio files in correct folders", 
                                displayTime=100)
            self.display_prompt("Find folders in SeqRec_master/audio_stims/",
                                displayTime=100)
            # exit the python interpreter
            sys.exit()
            
        else:
            # check if files (hopefully audio stims) in /audio_stims/
            for subfolder in os.listdir("SeqRec_master/audio_stims/"):
                if os.path.isdir("SeqRec_master/audio_stims/" + subfolder):
                    # if some subfolder is empty
                    if os.listdir("SeqRec_master/audio_stims/"+subfolder)==[]:
                        # display error
                        self.display_prompt("ERROR: Please put audio files" + 
                                        "in correct folders", displayTime=100)
                        self.display_prompt("At least one subfolder is empty", 
                                            displayTime=100)
                        self.display_prompt(("Find folders here >>> " + 
                                             str("SeqRec_master/audio_stims/")),
                                            displayTime=100)
                        sys.exit()

                        
    def WAV_folder_to_List(self, AorB, item):
        '''
        Look in a folder, take out all the WAVs we want, and assign them to list
        '''
        # Make sure AorB is actually a string (ie. "A" or "B")
        assert type(AorB)==str
        # A list we first dump all our paths to, which makes sorting easier
        smallList = []
        bigList = []
        i=0
        try:
            # loop through all the WAVs in a folder
            for path in os.listdir("SeqRec_master/audio_stims/" + item + "_" 
                                   + AorB + "/"):
                    smallList.append(path)
        except OSError:
            print "ERROR: folder of audio files not found"
            self.win.close()
            sys.exit()

        # This loop is how we keep speakers separate
        for speaker in self.speakers:
            bigList.append([])
            for WAVpath in smallList:
                # append WAVs which contain speaker name in path
                if speaker in WAVpath:
                    bigList[i].append("SeqRec_master/audio_stims/" + 
                                           item + "_" + AorB + "/" + WAVpath)
            i+=1
        return bigList

    
    def display_prompt(self, prompt, displayTime=30, selfPaced=True):
        '''
        Putting text on the screen. Function requires window, the text prompt,
        and how many frames we want window on screen
        '''
        # This loop draws and flips window each time around
        if selfPaced == True:
            visual.TextStim(self.win, text = prompt).draw()
            self.win.flip()
            event.waitKeys()
        else:
            for frameN in range(displayTime):
                # actually draw the window
                visual.TextStim(self.win, text = prompt).draw()
                # flip the window to the screen
                self.win.flip()
        # flip to buffer, so we don't have text on screen indefinitely
        self.win.flip()

        
    def play_list_WAVs(self, _list, isi):
        '''
        Loops through a list of WAV files and plays them with a given 
        inter-stimulus interval (ISI)
        '''
        try:
            for WAV in _list:
                # create sound object with all info needed
                mySound = sound.Sound(value=WAV, sampleRate=44100, bits=16, 
                                       name='', autoLog=True)
                # actually play the sound
                mySound.play()
                # You need the duration of the sound here, or else we play
                # overlappying sounds
                core.wait(mySound.getDuration()+isi)
        except:
            print "ERROR: audio files not found"
            self.win.close()
            sys.exit()

            
    def create_sequences(self, AandB_Paths, templateList):
        # list to store our output
        orderedWAVPaths = []
        # make lists of indices of speakers and tokens
        iSpeakers = range(len(AandB_Paths[0]))
        iTokens = range(len(AandB_Paths[0][0]))
        # initialize speaker variable just once
        speaker=0
        token=0
        currentSequence=0
        # pick a character string of type "A_A_B_A" out of the template list
        for seqName in templateList:
            orderedWAVPaths.append([])
            # this walks down the template string character by character
            for char in seqName:
                if char == "A":
                    AorB = 0
                elif char == "B":
                    AorB = 1
                else:
                    AorB = None
                    
                if AorB != None:
                    # randomly choose speaker after previous speaker is removed
                    newSpeakers = [i for i in iSpeakers if i != speaker]
                    speaker = random.choice(newSpeakers)
                    # randomly choose token after previous token is removed
                    newTokens = [i for i in iTokens if i != token]
                    token = random.choice(newTokens)
                    # append the WAV file to listOfPaths
                    orderedWAVPaths[currentSequence].append(
                        AandB_Paths[AorB][speaker][token])
            currentSequence += 1

        # initialize our lists for different levels
        token_2=[]; token_3=[]; token_4=[]; token_5=[]; token_6=[]

        for seq in orderedWAVPaths:
            # This loop passes through sequences, and tells us how long they are
            # Then we assign them to their appropriate level list so they can
            # be played in order.
            # First the 2-token sequences, then 3, etc.
            if len(seq)==2:
                token_2.append(seq)
            if len(seq)==3:
                token_3.append(seq)
            if len(seq)==4:
                token_4.append(seq)
            if len(seq)==5:
                token_5.append(seq)
            if len(seq)==6:
                token_6.append(seq)
        return [token_2, token_3, token_4, token_5, token_6]

                
    def familiarization_task(self, keyPress, AandB_Paths):
        '''
        when the participant presses a key, play the corresponding stimulus
        '''
        # get indexes for speakers and tokens
        iSpeakers = range(len(AandB_Paths[0]))
        iTokens = range(len(AandB_Paths[0][0]))
        # check if participant pressed the left arrow
        if keyPress == ["left"]:
            # set WAVlist to the 'a' tokens 
            AorB = 0
            # set the position of the circle to be shown on left side of screen
            pos = [-300,0]
        if keyPress == ["right"]:
            AorB = 1
            pos = [300,0]
        # pick a random speaker
        speaker = random.choice(iSpeakers)
        # pick a random token
        token = random.choice(iTokens)
        # get the path of the given WAV file
        WAV = AandB_Paths[AorB][speaker][token]
        # create a sound object
        mySound = sound.Sound(value=WAV,sampleRate=44100,bits=16,autoLog=True)
        # play the sound
        mySound.play()
        # put up the circle on the screen for a little while
        for frameN in range(20):
            myStim = visual.GratingStim(self.win, tex=None, mask="gauss", 
                                        size=300, color = "green", pos=pos)
            myStim.draw()           
            self.win.flip()
        self.win.flip()
        
    
    def testing_phase(self, AandB_Paths):
        '''
        Participant must correctly identify a given number of stimuli
        in a row to proceed. A circle is desplayed to participant to 
        indicate progress.
        '''
        circleRadius=280
        outerCircle = visual.Circle(self.win, radius = circleRadius, edges = 64,
                                    lineColor="green", fillColor="green")
        innerCircle = visual.Circle(self.win, radius = circleRadius, edges = 64,
                                    lineColor="green", fillColor="green", 
                                    contrast=.15)
        i = 0
        while i < self.testCutOff:
            if i == 0:
                visual.Circle(self.win, radius = circleRadius, edges = 64, 
                              lineColor="green", fillColor="green",
                              contrast=.15).draw()
                self.win.flip()
            else:
                outerCircle.draw()
                innerCircle.setRadius(circleRadius-
                                      (circleRadius/self.testCutOff)*i)
                innerCircle.draw()
                self.win.flip()
            # pick randomly the list of 'A' or 'B' tokens
            AorB = random.choice(range(len(AandB_Paths)))
            # pick random speaker
            speaker= random.choice(range(len(AandB_Paths[0])))
            # pick random token
            token= random.choice(range(len(AandB_Paths[0][0])))
            # assign audio file path to object WAV
            WAV = AandB_Paths[AorB][speaker][token]
            # create the sound object with the audio stimulus WAV
            mySound= sound.Sound(value=WAV, sampleRate=44100, bits=16, name='',
                                  autoLog=True)
            # play the sound object 
            mySound.play()
            # wait until the sound is through playing
            core.wait(mySound.getDuration())
            # wait for key press and save it to keyPress
            keyPress = event.waitKeys()
            # check if the answer was correct - A==0 and B==1
            if ((keyPress == ["left"] and AorB==0) or
                (keyPress == ["right"] and AorB==1)):
                # participant gets credit for the answer
                i+=1
                # fill in more of the circle to show progress
                for frameN in range(15):
                    outerCircle.draw()
                    innerCircle.setRadius(circleRadius-
                                          (circleRadius/self.testCutOff)*i)
                    innerCircle.draw()
                    self.win.flip()
            # the participant got it wrong
            else:
                # sorry, participant back to zero :(
                i=0
            outerCircle.draw()
            innerCircle.setRadius(circleRadius-(circleRadius/self.testCutOff)*i)
            innerCircle.draw()
            self.win.flip()
            # wait before we play next WAV file
            core.wait(self.testISI)

            
    def play_one_level(self, level):
        '''
        Play one level of sequences as described in Dupoux et al. 2001. 
        The kinds of sequences can be found in the template.py file
        '''
        responses=[]
        # randomize order of sequences
        random.shuffle(level)
        # pull out one sequence
        for seq in level:
            # play each sequence in list
            self.play_list_WAVs(seq,self.mainISI)
            # create sound object (just a beep to signal end of sequence)
            E = sound.Sound(value="E", secs=.3, bits=16, name='',
                               autoLog=True)
            # actually play the beep
            E.setVolume(.5)
            E.play()
            # wait to collect responses
            core.wait(E.getDuration())
            # gather the responses
            responses.append(self.collect_responses(seq,waitingTime=5))
            # wait a half of a second before next level
            core.wait(.5)
        return responses

    
    def collect_responses(self, _list, waitingTime):
        '''
        After the participant hears the sequence of WAVs, we want to collect and
        save their key presses and the name of the file they heard. This way
        we will later be able to check whether or not any given answer was
        correct.
        '''
        # A list to collect responses and WAV paths for every sequence
        responses=[]
        boxes = [.15]*len(_list)
        i=0
        for WAV in _list:
            # full path is unneccesary - only save item and speaker
            shortPath= os.path.basename(WAV)
            myTex = numpy.array([boxes])
            myStim = visual.GratingStim(self.win, tex=myTex, mask=None,
                                size=[100*len(_list),50], color = "green")
            myStim.draw()
            self.win.flip()
            # Give the participants a time limit to respond
            timer = core.CountdownTimer(waitingTime)
            # Loop runs unless timelimit exceeded
            while timer.getTime() > 0:
                # wait for keypress and save it
                keyPress = event.waitKeys()
                # append key press and WAV filename to the list
                responses.append([shortPath,keyPress[0]])
                # without 'break' you are stuck in loop even after a key press
                break

            # increment boxes on the screen to show progress for each keypress
            boxes[i]=1
            myTex = numpy.array([boxes])
            myStim = visual.GratingStim(self.win, tex=myTex, mask=None, 
                                size=[100*len(_list),50], color = "green")
            myStim.draw()
            self.win.flip()
            i+=1
        core.wait(.5)
        self.win.flip()
        return responses
    
    def run_experiment(self, participantID):
        # Now we've passed our safety checks, pick a contrast and run it!
        # First, randomize all contrasts except for the first, control contrast
        contrast1 = [self.contrasts[0]]
        contrastsRest = self.contrasts[1:]
        random.shuffle(contrastsRest)
        self.contrasts = contrast1 + contrastsRest
        # using the control+random list, start the experiment
        for contrastIndex,contrast in enumerate(self.contrasts):
            
            # pull out all A stimuli and assign them to list 'A' and 'B'
            A = self.WAV_folder_to_List("A", contrast[0])
            B = self.WAV_folder_to_List("B", contrast[1])
            AandB_Paths=[A,B]

            # PROMPT FORCED LISTENS
            self.display_prompt("You will now hear two words...\n\n"+
                                "Pay attention to what the words sound like.\n"+
                                "\n\n\n\nPress SPACE to move on.",
                                selfPaced=True)
            core.wait(1)
            
            forcedListens = ["left", "right"]*(self.numForcedListens/2)
            random.shuffle(forcedListens)

            # RUN FORCED LISTENS
            for i in forcedListens:
                self.familiarization_task([i], AandB_Paths)
                core.wait(.75)

            # PROMPT FAMILIARIZATION
            self.display_prompt("Time for some practice...\n\n"+
                                "Press an arrow to hear a word.\n"+
                                "When you are done,\n"+
                                "press the SPACE bar.\n"+
                                "\n\n\n\nPress SPACE to move on.",
                                selfPaced=True)
            core.wait(.5)

            self.display_prompt("Press either LEFT or RIGHT arrow.",
                                displayTime=50,selfPaced=False)
            core.wait(.5)

            # RUN FAMILIARIZATION
            while 1:
                # wait for keypress
                keyPress = event.waitKeys()
                # participant can press spacebar to move on to testing
                if keyPress == ["space"]:
                    break
                else:
                    # they (hopefully) pressed either A or B, so play it
                    self.familiarization_task(keyPress, AandB_Paths)


            # PROMPT TESTING
            self.display_prompt("Time for a little test...\n\n"+
                                "When you hear a word,\n"+
                                "press the correct arrow.\n\n"+
                                "You need to get 7 correct in-a-row.\n"+
                                "\n\n\n\nPress SPACE to move on.",
                                selfPaced=True)
            core.wait(.5)
            
            # RUN TESTING
            self.testing_phase(AandB_Paths)


            # PROMPT SEQREC
            self.display_prompt("Congrats, you did it!", displayTime=70,
                                selfPaced=False)
            core.wait(.5)

            self.display_prompt("Now it's time for the fun stuff!",
                                displayTime=70, selfPaced=False)
            core.wait(.5)
            
            self.display_prompt("You now will hear sequences\n"+
                                "of these same two words,\n"+
                                "and you have to remember their order.\n"+
                                "\n\n\n\nPress SPACE to move on.",
                                selfPaced=True)
            core.wait(.5)

            self.display_prompt("The sequence will play\n"+
                                "and then you hear a beep"+
                                "\n\n\n\nPress SPACE to move on.",
                                selfPaced=True)
            core.wait(.5)

            self.display_prompt("After the beep, press the\n"+
                                "arrows in the same sequence."+
                                "\n\n\n\nPress SPACE to move on.",
                                selfPaced=True)
            core.wait(.5)

            # RUN SEQREC
            allLevels = self.create_sequences(AandB_Paths, templateList)
            for level in allLevels[:2]:
                self.responses.append(self.play_one_level(level))
                self.mario()
                self.display_prompt("Great job!", displayTime=70,
                                    selfPaced=False)
                core.wait(1)

            if contrastIndex < (len(self.contrasts)-1):
                self.display_prompt("Time for some new words!"+
                                    "\n\n\n\nPress SPACE to move on.",
                                    selfPaced=True)
                core.wait(.5)
            else:
                # this displays at very end of experiment
                self.display_prompt("You're all done!\nThanks for your Time!",
                                    displayTime=70, selfPaced=False)

        with open((str(participantID) + '_seqrec_results.txt'),'a') as f:
            for level in self.responses:
                for sequence in level:
                    f.write("%s\n" % sequence)


    def mario(self):
        C4 = sound.Sound(value=261.63, secs=.15, bits=16, name='',
                           autoLog=True)
        E4 = sound.Sound(value=329.63, secs=.15, bits=16, name='',
                           autoLog=True)
        G3 = sound.Sound(value=196.00, secs=.15, bits=16, name='',
                           autoLog=True)
        G4 = sound.Sound(value=392.00, secs=.15, bits=16, name='',
                           autoLog=True)
        C4.setVolume(.5)
        E4.setVolume(.5)
        G3.setVolume(.5)
        G4.setVolume(.5)
        
        E4.play(); core.wait(.16)
        E4.play(); core.wait(.20)
        E4.play(); core.wait(.3)
        C4.play(); core.wait(.16)
        E4.play(); core.wait(.3)
        G4.play(); core.wait(.5)
        G3.play(); core.wait(.4)

        
    def run(self):
        self.check_dir()
        participantID = raw_input('Enter participant ID: ')
        # test small screen
        self.win = visual.Window(self.displayRes, fullscr=False, units="pix", 
                                 allowGUI=True,winType="pyglet")
        # create the display window for the experiment
        # self.win = visual.Window(fullscr=True, units="pix", 
        #                  allowGUI=True,winType="pyglet") 
        self.run_experiment(participantID)
        self.win.close()
        sys.exit()


if __name__ == "__main__":
    S = SeqRec()
    S.run()
