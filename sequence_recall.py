# -*- coding: utf-8 -*-
'''

USAGE: 
$ python sequence_recall.py

DEPENDENCIES:
template.py

FILE STRUCTURE:

/
    sequence_recall.py
    template.py
    SeqRec_master/
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

As of now, my filenames for the audio files are of the form: 
    <condition>_<speaker>_<tokenNumber>_<A|B>.wav 
    e.g. kupo_erica_1_A.wav

'''

from template import templateList                                               # from template.py
from psychopy import visual, event, sound, core                                 # Visual displays prompts, event gets keypresses, 
                                                                                # sound plays WAVs, core will shut us down
import os                                                                       # for listing contents of a directory
import re                                                                       # for regex
import random                                                                   # helps us ranomize stimuli presentation
import sys
import numpy




class Seqrec():
    def __init__(self):
        self.templateList=templateList
        self.displayRes= [800,800]                                      
        self.speakers= ["_erica_","_josh_","_van_"]                             # My WAV stimuli were recorded by 3 speakers, 
                                                                                # this helps randomize them when we compile sequences
        #self.contrastList=[["gabo","gaabo"],["pyko","poeko"],["mipa","mipa"],
        #                                     ["guna","gunya"],["kupo","kuvo"]]
        self.contrastList=[["kupo","kuvo"]]                                     # testing list
        self.responses=[]
        self.win = visual.Window(self.displayRes, fullscr=False, units="pix", 
                                 allowGUI=True,winType="pyglet")                # create the display window for the experiment 
                                                                                # (an object called 'win') with all the info it needs
        self.check_dir()
        self.run_experiment()
        self.win.close()
        sys.exit()

    def check_dir(self):
        if not os.path.exists("SeqRec_master/"):                                # Check if the directory SeqRec_master/ exists, 
                                                                                # if it doesn't, this loop creates it
            for contrast in self.contrastList:                                  # loop through the contrasts you filled in the 
                                                                                # variable section (self.contrastList)
                os.makedirs("SeqRec_master/audio_stims/" + contrast[0] + "_A/") # make a subfolder for the A contrast
                os.makedirs("SeqRec_master/audio_stims/" + contrast[1] + "_B/") # make a subfolder for the B contrast
            self.display_prompt("ERROR: Put audio files in correct folders", 
                                displayTime=100)                                # give the experimenter an error message
            self.display_prompt("Find folders in SeqRec_master/audio_stims/",
                                displayTime=100)                                # Show where the subfolders are
            sys.exit()                                                          # exit the python interpreter
        else:
            for subfolder in os.listdir("SeqRec_master/audio_stims/"):          # This loop checks to see there is something (should 
                                                                                # be WAV files) in the subfolders of /audio_stims/
                if os.path.isdir("SeqRec_master/audio_stims/" + subfolder):     # make sure we are look into directories, not files
                    if os.listdir("SeqRec_master/audio_stims/"+subfolder)==[]:  # if the subfolder is empty
                        self.display_prompt("ERROR: Please put audio files" + 
                                        "in correct folders", displayTime=100)  # display error
                        self.display_prompt("At least one subfolder is empty", 
                                            displayTime=100)                    # more error
                        self.display_prompt(("Find folders here >>> " + 
                                             str("SeqRec_master/audio_stims/")),
                                            displayTime=100)                    # show where folders are
                        sys.exit()
    
    def WAV_folder_to_List(self, AorB, item):                                   # This looks in a folder, takes out all the WAVs 
                                                                                # we want, and assigns them to a list
        assert type(AorB)==str                                                  # Make sure AorB is actually "A" or "B"
        smallList = []                                                          # A list we first dump all our paths to, 
                                                                                # makes sorting easier
        self.bigList = []
        i=0
        try:
            for path in os.listdir("SeqRec_master/audio_stims/" + item + "_" 
                                   + AorB + "/"):                                   # loop through all the WAVs in a folder
                    smallList.append(path)                                          # append each of those WAVs to smallList
        except OSError:
            print "ERROR: folder of audio files not found"
            self.win.close()
            sys.exit()

        for speaker in self.speakers:                                           # This loop is how we keep speakers separate
            self.bigList.append([])
            for WAVpath in smallList:
                if speaker in WAVpath:
                    self.bigList[i].append("SeqRec_master/audio_stims/" + 
                                           item + "_" + AorB + "/" + WAVpath)   # Only append those WAVs which contain the speaker 
                                                                                # name in the path
            i+=1

    
    def display_prompt(self, prompt, displayTime=30):                           # Putting text on the screen, it needs window, 
                                                                                # prompt, and how many frames we want window up
        for frameN in range(displayTime):                                       # This loop draws and flips window each time around
            visual.TextStim(self.win, text = prompt).draw()                     # actually draw the window
            self.win.flip()                                                     # flip the window to the screen
        self.win.flip()                                                         # flip to the buffer, which is blank, so we don't have
                                                                                # the text sitting on the screen indefinitely
    
    def play_list_WAVs(self, _list, isi):                                       # Loops through a list of WAVs and plays them with 
        try:                                                                                # a given inter-stimulus interval (isi)
            for WAV in _list:
                my_sound = sound.Sound(value=WAV, sampleRate=44100, bits=16, 
                                       name='', autoLog=True)                       # create sound object with all info needed
                my_sound.play()                                                     # actually play the sound
                core.wait(my_sound.getDuration()+isi)                               # You need the duration of the sound here, 
                                                                                    # or else we play overlappying sounds
        except:
            print "ERROR: audio files not found"
            self.win.close()
            sys.exit()
    
    def play_one_level(self, level, isi=.08):                                   # Play one level of sequences
        random.shuffle(level)                                                   # do the shuffle
        self.levelList=[]                                                       # create an empty list
        for seq in level:                                                       # pull out one sequence
            self.play_list_WAVs(seq[1:],isi)                                    # the the list, but starting from the second element,
                                                                                # the first element is just a character string of 
                                                                                # type "A_A_B_A"

            beep = sound.Sound(value="E", secs=.3, bits=16, name='',            # create sound object (just a beep to signal end
                               autoLog=True)                                    # of sequence)
            beep.play()                                                         # actually play the beep
            core.wait(beep.getDuration()+isi)                                   # wait to collect responses
            self.collect_responses(seq,waitingTime=5)                           # gather the responses
            core.wait(.5)                                                       # wait a half of a second before next level
    
    def create_sequences(self):
        listOfPaths=[]                                                          # make an empty list
        speakerA=0                                                              # these speaker and token variables are what 
                                                                                # we use to shuffle our WAV paths
        tokenA=0
        speakerB=0
        tokenB=0
        currentSequence=0                                                       # our counter for sequences
        for seqName in self.templateList:                                       # pick a character string of type "A_A_B_A" out of 
                                                                                # the template list
            listOfPaths.append([seqName])                                       # append the character string to as a sublist 
                                                                                # with one element to the superlist listOfPaths
            for item in seqName:                                                # this walks down the character string seqName
                                                                                # character by character
                if item == "A":                                                 # if the char is an "A"
                    if speakerA > len(self.AandB_Paths[0])-1:                   # This makes sure we don't index out of the list. 
                                                                                # If speakerA == x, AandBPaths[x] doesn't exist,
                                                                                # we get an error
                        speakerA = 0                                            # reset the speaker counter
                        tokenA += 1                                             # start on a new batch of tokens, since if we went 
                                                                                # through all the (for example) second tokens for 
                                                                                # the speakers, we need to get on the third
                    if tokenA > len(self.AandB_Paths[0][0])-1:                  # if we're out of range with regards to tokens,
                        tokenA = 0                                              # reset the counter
                    listOfPaths[currentSequence].append(
                        self.AandB_Paths[0][speakerA][tokenA])                  # finally, we append the WAV file to listOfPaths
                    speakerA += 1                                               # on to the next speakerA
                if item == "B":                                                 # same process now for the 'b' tokens
                    if speakerB > len(self.AandB_Paths[1])-1:
                        speakerB = 0
                        tokenB += 1
                    if tokenB > len(self.AandB_Paths[1][0])-1:
                        tokenB = 0
                    listOfPaths[currentSequence].append(
                        self.AandB_Paths[1][speakerB][tokenB])
                    speakerB += 1
            currentSequence += 1                                                # On to the next sequence
        self.token_2=[]
        self.token_3=[]
        self.token_4=[]
        self.token_5=[]
        self.token_6=[]
        for seq in listOfPaths:                                                 # This loop passes through the sequence (sublists of 
                                                                                # listOfPaths), and tells us how long the sequences
            if len(seq)==3:                                                     # are. Then we assign them to their appropriate
                self.token_2.append(seq)                                        # level list so they can be played in order. 
                                                                                # First the 2-token sequences, then 3, etc. 
            if len(seq)==4:
                self.token_3.append(seq)
            if len(seq)==5:
                self.token_4.append(seq)
            if len(seq)==6:
                self.token_5.append(seq)
            if len(seq)==7:
                self.token_6.append(seq)
    
    def familiarization_task(self, keyPress):                                   # we need a key press to evaluate, and if we collect 
                                                                                # it outside the function, we can have the function 
                                                                                # in an infinite loop that the participant can break
        if keyPress == ["left"]:                                                # check if they pressed the left arrow
            WAVlist=self.a                                                      # set WAVlist to the 'a' tokens (this whole task 
                                                                                # relies on the 'a' and 'b' distinction, can be 
                                                                                # thought of as 'cat' and 'dog' like before)
            pos=[-300,0]
        if keyPress == ["right"]:                                               # check if they pressed the right arrow
            WAVlist=self.b                                                      # set the WAVlist to the 'b' tokens 
            pos=[300,0]
        speaker= random.choice(range(len(self.AandB_Paths[1])))                 # pick a random speaker
        token= random.choice(range(len(self.AandB_Paths[1][1])))                # pick a random token
        WAV = WAVlist[speaker][token]                                           # assign the actual path to WAV
        my_sound= sound.Sound(value=WAV, sampleRate=44100, bits=16, name='', 
                              autoLog=True)                                     # create a sound object with the audio stimulus WAV
        my_sound.play()                                                         # play the sound
        for frameN in range(20):
            myStim = visual.GratingStim(self.win, tex=None, mask="gauss", 
                                        size=300, color = "green", pos=pos)
            myStim.draw()           
            self.win.flip()
        self.win.flip()
    
    def testing_phase(self, isi=.6, testCutoff=7, i=0):                         # isi = inter-stimulus interval
        outerCircle = visual.Circle(self.win, radius = 280, edges = 64,
                                    lineColor="green", fillColor="green")
        innerCircle = visual.Circle(self.win, radius = 280, edges = 64,
                                    lineColor="green", fillColor="green", 
                                    contrast=.15)
        while i < testCutoff:
            if i == 0:
                visual.Circle(self.win, radius = 280, edges = 64, 
                              lineColor="green", fillColor="green",
                              contrast=.15).draw()
                self.win.flip()
            else:
                outerCircle.draw()
                innerCircle.setRadius(280-40*i)
                innerCircle.draw()
                self.win.flip()
            WAVlist = random.choice(range(len(self.AandB_Paths)))               # pick randomly the list of 'a' or 'b' tokens
            speaker= random.choice(range(len(self.AandB_Paths[1])))             # pick random speaker
            token= random.choice(range(len(self.AandB_Paths[1][1])))            # pick random token
            WAV = self.AandB_Paths[WAVlist][speaker][token]                     # assign audio file path to object WAV
            my_sound= sound.Sound(value=WAV, sampleRate=44100, bits=16, name='',
                                  autoLog=True)                                 # create the sound object with the audio stimulus WAV
            my_sound.play()                                                     # play the sound object 
            core.wait(my_sound.getDuration())                                   # wait until the sound is through playing
            keyPress = event.waitKeys()                                         # wait for key press and save it to keyPress
            if keyPress == ["left"]:                                            # check if the left arrow was pressed
                if bool(re.search("A.wav", WAV)):                               # check if the WAV path was an 'a' token
                    i+=1                                                        # increment i by one, making sure the participant
                                                                                # gets credit for the answer
                    for frameN in range(15):
                        outerCircle.draw()
                        innerCircle.setRadius(280-40*i)
                        innerCircle.draw()
                        visual.TextStim(self.win, "CORRECT").draw()             # project "CORRECT" on the screen
                        self.win.flip()
                else:
                    self.display_prompt("WRONG")                                # sorry, participant
                    i=0                                                         # back to zero :(
            if keyPress == ["right"]:                                           # same loop as above, but for the 'b' tokens
                if bool(re.search("B.wav", WAV)):
                    i+=1                                                        # increment i by one, making sure the participant
                                                                                # gets credit for the answer
                    for frameN in range(15):
                        outerCircle.draw()
                        innerCircle.setRadius(280-40*i)
                        innerCircle.draw()
                        visual.TextStim(self.win, "CORRECT").draw()             # project "CORRECT" on the screen
                        self.win.flip()
                else:
                    self.display_prompt("WRONG")
                    i=0
            outerCircle.draw()
            innerCircle.setRadius(280-40*i)
            innerCircle.draw()
            self.win.flip()    
            core.wait(isi)                                                      # wait before we play next WAV file
    
    def collect_responses(self, _list, waitingTime):                            # After the participant hears the sequence of WAVs, 
                                                                                # we want to collect and save some key presses
        oneSeqList=[]                                                           # A list to collect responses and WAV paths for
                                                                                # every sequence
        boxes = [.15]*len(_list[1:])
        i=0
        for WAV in _list[1:]:                                                   # The loop that appends our WAV paths to oneSeqList
            regexpr="/audio_stims/.*[.]wav"                                     # The full path is unneccesary, so we just get the
                                                                                # important info coded in filename (item and speaker)
            matchObject = re.search(regexpr, WAV)                               # some regex magic
            shortPath= matchObject.group()                                      # more regex magic which leads to a shortened path
            myTex = numpy.array([boxes])
            myStim = visual.GratingStim(self.win, tex=myTex, mask=None,
                                size=[100*len(_list[1:]),50], color = "green")
            myStim.draw()
            self.win.flip()
            timer = core.CountdownTimer(waitingTime)                            # Give the participants a time limit
            while timer.getTime() > 0:                                          # Loop runs unless timelimit exceeded
                keyPress = event.waitKeys()                                     # wait for keypress and save it to keyPress
                oneSeqList.append([shortPath,keyPress[0]])                      # append the key press to the list
                break                                                           # break from loop (without this you are stuck in 
                                                                                # the loop until time runs out, even after key press)
            boxes[i]=1
            myTex = numpy.array([boxes])
            myStim = visual.GratingStim(self.win, tex=myTex, mask=None, 
                                size=[100*len(_list[1:]),50], color = "green")
            myStim.draw()
            self.win.flip()
            i+=1
        core.wait(.5)
        self.win.flip()
        self.levelList.append(oneSeqList)                                       # append both the key presses and the WAV files to
                                                                                # the globally defined levelList (one per level)
    
    def run_experiment(self):
        for i in self.contrastList:                                             # Now we've passed our safety checks, pick a contrast
            print i
                                                                                # and run it!
            itemA = i[0]                                                        # assign the A item
            itemB = i[1]                                                        # assign the B item
            self.WAV_folder_to_List("A", itemA)                                 # pull out all A stimuli
            self.a=self.bigList                                                 # and assign them to list a
            self.WAV_folder_to_List("B", itemB)                                 # pull out all B stimuli
            self.b=self.bigList                                                 # and assign them to list b
            self.AandB_Paths=[self.a,self.b]                                    # make our super list of a and b paths
            self.display_prompt("press either a or b")                          # begin familiarzation with prompt
            core.wait(1)
            #
            while 1:
                keyPress = event.waitKeys()                                     # check for keypress here
                if keyPress == ["space"]:                                       # participant can press spacebar to exit
                    break                                                       # break from loop
                else:                                                           # otherwise...
                    self.familiarization_task(keyPress)                         # another stimulus for familiarization 
            core.wait(1)
            #
            self.testing_phase()						# run the testing phase
            #
            self.create_sequences()                                             # create sequences from our template and stimuli
            self.display_prompt("listen to the sounds and push the buttons!")   # start sequence recall with prompt
            core.wait(1)
            #
            self.play_one_level(self.token_2)                                   # play a level
            token2List = self.levelList                                         # save level to its own list
            core.wait(1)
            #
            self.play_one_level(self.token_3)
            token3List = self.levelList
            core.wait(1)
            #
            self.contrastList = [token2List,token3List]                         # create a master list out of all the level lists
            self.responses.append(self.contrastList)

        with open('results.txt','a') as f:
            for item in self.responses:
                f.write("%s\n" % item)

expObj = Seqrec()
