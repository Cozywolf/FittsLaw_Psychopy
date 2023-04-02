import random
import math
import re  # Special characters check
import pylsl as lsl  # Import LabStreamingLayer for sending the marker
import tkinter as tk
# Import Psychopy, an open-source psychological experiment application.
from psychopy import core, visual, gui, event, data, monitors
import fittsLawFunctions as fl
import os
if not os.path.exists('./data/'):
    os.mkdir('./data/')


def main():
    print("Initiating...")

    # Set up LabStreamingLayer stream.
    info = lsl.StreamInfo(name='fittslaw_stream', type='Markers', channel_count=1,
                          channel_format='int32', source_id='fittslaw_stream_001')
    outlet = lsl.StreamOutlet(info)  # Broadcast the stream.
    print("LSL stream created")
    # Define event markers
    markers = {
        'sectionstart': [1],
        'conditionstart': [2],
        'clickstart': [3],
        'clickend': [4],
        'conditionend': [5],
        'sectionend': [6],
        'directionchange': [7],
        'test': [99],
        'start': [50],
        'end': [60],
    }
    print("LSL markers defined")

    # present a dialogue to change params
    dlg = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlg.addText('Participant & Condition info')
    dlg.addField(label='Subject name/number:')
    dlg.addField(label='Input Device:')
    dlg.addField(label='Speed setting:')
    dlg.addText('Experiment settings')
    dlg.addField(initial=1920, label='Display width (px):')
    dlg.addField(initial=1080, label='Display height (px):')
    dlg.addField(initial='Multi-dimensional discrete', choices=['1-dimensional serial', '1-dimensional discrete', '2-dimensional serial',
                 '2-dimensional discrete', 'Multi-dimensional serial', 'Multi-dimensional discrete', 'Random spawn discrete'], label='Test type:')
    dlg.addField(initial='Yes', choices=['Yes', 'No'], label='Fullscreen?')
    dlg.addField(initial=0, label='Monitor #:')

    dlg.show()
    if dlg.OK:
        if (re.match("^[a-zA-Z0-9_]*$", dlg.data[0]) and re.match("^[a-zA-Z0-9_]*$", dlg.data[1]) and re.match("^[a-zA-Z0-9_]*$", dlg.data[2])):
            print("Setup completed!")  # save params to file for next time
        else:
            dlgerror = gui.Dlg(title='Do not use special characters')
            dlgerror.addText(
                'Use only alphabets, numbers, and underline for the Subject, Device, and Speed fields!')
            dlgerror.addText('Use only numbers for display width and height!')
            dlgerror.show()
            if dlgerror.OK:
                return
            else:
                return
    else:
        return  # the user hit cancel to exit

    # Convert the display width and height from str to int
    winWidth = int(dlg.data[3])
    winHeight = int(dlg.data[4])
    screen = int(dlg.data[7])

    # Set fullscreen
    if (dlg.data[6] == 'Yes'):
        full = True
    else:
        full = False

    # Set the display area to square shape
    if (winWidth > winHeight):
        displaySize = winHeight
    else:
        displaySize = winWidth

    # Define test type specific dialogue boxes
    dlgMultiDis = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlgMultiDis.addText('Multi-dimensional discrete test')
    dlgMultiDis.addField(initial='4', choices=[
                         '1', '2', '3', '4', '5', '6', '7'], label='Size variation?')
    dlgMultiDis.addField(initial='3', choices=[
                         '1', '2', '3', '4', '5', '6', '7'], label='Distance variation?')
    dlgMultiDis.addField(initial='8', choices=['7', '8', '9', '10', '11', '12', '13', '14', '15',
                         '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'], label='Angle variation?')
    dlgMultiDis.addField(initial='No repeat', choices=[
                         'No repeat', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label='Repetition?')
    dlgMultiDis.addField(initial='Yes', choices=[
                         'Yes', 'No'], label='Target hint?')
    dlgMultiDis.addField(initial='Yes', choices=[
                         'Yes', 'No'], label='Center the cursor for each trial?')

    dlgMultiSer = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlgMultiSer.addText('Multi-dimensional serial test')
    dlgMultiSer.addField(initial='4', choices=[
                         '1', '2', '3', '4', '5', '6', '7'], label='Size variation?')
    dlgMultiSer.addField(initial='3', choices=[
                         '1', '2', '3', '4', '5', '6', '7'], label='Distance variation?')
    dlgMultiSer.addField(initial='7', choices=[
                         '7', '9', '11', '13', '15', '17', '19', '21', '23', '25'], label='Angle variation?')
    dlgMultiSer.addField(initial='No repeat', choices=[
                         'No repeat', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label='Repetition?')

    dlg2DDis = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlg2DDis.addText('2-dimensional discrete test')
    dlg2DDis.addField(initial='4', choices=[
                      '1', '2', '3', '4', '5', '6', '7'], label='Size variation?')
    dlg2DDis.addField(initial='3', choices=[
                      '1', '2', '3', '4', '5', '6', '7'], label='Distance variation?')
    dlg2DDis.addField(initial='10', label='Trials per condition?')
    dlg2DDis.addField(initial='No repeat', choices=[
                      'No repeat', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label='Repetition?')
    dlg2DDis.addField(initial='Yes', choices=[
                      'Yes', 'No'], label='Target hint?')
    dlg2DDis.addField(initial='Yes', choices=[
                      'Yes', 'No'], label='Center the cursor for each trial?')

    dlg2DSer = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlg2DSer.addText('2-dimensional serial test')
    dlg2DSer.addField(initial='4', choices=[
                      '1', '2', '3', '4', '5', '6', '7'], label='Size variation?')
    dlg2DSer.addField(initial='3', choices=[
                      '1', '2', '3', '4', '5', '6', '7'], label='Distance variation?')
    dlg2DSer.addField(initial='10', label='Trials per condition?')
    dlg2DSer.addField(initial='No repeat', choices=[
                      'No repeat', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label='Repetition?')

    dlg1DDis = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlg1DDis.addText('1-dimensional discrete test')
    dlg1DDis.addField(initial='4', choices=[
                      '1', '2', '3', '4', '5', '6', '7'], label='Size variation?')
    dlg1DDis.addField(initial='3', choices=[
                      '1', '2', '3', '4', '5', '6', '7'], label='Distance variation?')
    dlg1DDis.addField(initial='10', label='Trials per condition?')
    dlg1DDis.addField(initial='Horizontal', choices=[
                      'Horizontal', 'Vertical'], label='Direction')
    dlg1DDis.addField(initial='No repeat', choices=[
                      'No repeat', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label='Repetition?')
    dlg1DDis.addField(initial='Yes', choices=[
                      'Yes', 'No'], label='Target hint?')
    dlg1DDis.addField(initial='Yes', choices=[
                      'Yes', 'No'], label='Center the cursor for each trial?')

    dlg1DSer = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlg1DSer.addText('1-dimensional serial test')
    dlg1DSer.addField(initial='4', choices=[
                      '1', '2', '3', '4', '5', '6', '7'], label='Size variation?')
    dlg1DSer.addField(initial='3', choices=[
                      '1', '2', '3', '4', '5', '6', '7'], label='Distance variation?')
    dlg1DSer.addField(initial='10', label='Trials per condition?')
    dlg1DSer.addField(initial='Horizontal', choices=[
                      'Horizontal', 'Vertical'], label='Direction')
    dlg1DSer.addField(initial='No repeat', choices=[
                      'No repeat', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label='Repetition?')

    dlgRanS = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlgRanS.addText('Random spawn discrete test')
    dlgRanS.addField(initial='4', choices=[
                     '1', '2', '3', '4', '5', '6', '7'], label='Size variation?')
    dlgRanS.addField(initial='3', choices=[
                     '1', '2', '3', '4', '5', '6', '7'], label='Distance variation?')
    dlgRanS.addField(initial='10', label='Trials per condition?')
    dlgRanS.addField(initial='No repeat', choices=[
                     'No repeat', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label='Repetition?')
    dlgRanS.addField(initial='Yes', choices=[
                     'Yes', 'No'], label='Target hint?')

    # Test type specific dialogue with sizes, distances, and angles setups
    if (dlg.data[5] == '2-dimensional serial'):
        dlg2DSer.show()
        if dlg2DSer.OK:
            print('Proceed to in-detail setting!')
            sizeSet = fl.sizedef(int(dlg2DSer.data[0]))
            distanceSet = fl.distancedef(displaySize, int(dlg2DSer.data[1]))
            trial = int(dlg2DSer.data[2])
            repetition = fl.repeatCount(dlg2DSer.data[3])
        else:
            return
    elif (dlg.data[5] == '2-dimensional discrete'):
        dlg2DDis.show()
        if dlg2DDis.OK:
            print('Proceed to in-detail setting!')
            sizeSet = fl.sizedef(int(dlg2DDis.data[0]))
            distanceSet = fl.distancedef(displaySize, int(dlg2DDis.data[1]))
            trial = int(dlg2DDis.data[2])
            repetition = fl.repeatCount(dlg2DDis.data[3])
            if (dlg2DDis.data[4] == 'Yes'):
                hint = True
            else:
                hint = False
            if (dlg2DDis.data[5] == 'Yes'):
                centering = True
            else:
                centering = False
        else:
            return

    elif (dlg.data[5] == '1-dimensional serial'):
        dlg1DSer.show()
        if dlg1DSer.OK:
            print('Proceed to in-detail setting!')
            sizeSet = fl.sizedef(int(dlg1DSer.data[0]))
            distanceSet = fl.distancedef(displaySize, int(dlg1DSer.data[1]))
            trial = int(dlg1DSer.data[2])
            direction = dlg1DSer.data[3]
            repetition = fl.repeatCount(dlg1DSer.data[4])
        else:
            return

    elif (dlg.data[5] == '1-dimensional discrete'):
        dlg1DDis.show()
        if dlg1DDis.OK:
            print('Proceed to in-detail setting!')
            sizeSet = fl.sizedef(int(dlg1DDis.data[0]))
            distanceSet = fl.distancedef(displaySize, int(dlg1DDis.data[1]))
            trial = int(dlg1DDis.data[2])
            direction = dlg1DSer.data[3]
            repetition = fl.repeatCount(dlg1DDis.data[4])
            if (dlg1DDis.data[5] == 'Yes'):
                hint = True
            else:
                hint = False
            if (dlg1DDis.data[6] == 'Yes'):
                centering = True
            else:
                centering = False
        else:
            return

    elif (dlg.data[5] == 'Multi-dimensional serial'):
        dlgMultiSer.show()
        if dlgMultiSer.OK:
            print('Proceed to in-detail setting!')
            sizeSet = fl.radiusdef(int(dlgMultiSer.data[0]))
            distanceSet = fl.distancedef(displaySize, int(dlgMultiSer.data[1]))
            angleSet = fl.angledef(int(dlgMultiSer.data[2]))
            repetition = fl.repeatCount(dlgMultiSer.data[3])
        else:
            return

    elif (dlg.data[5] == 'Multi-dimensional discrete'):
        dlgMultiDis.show()
        if dlgMultiDis.OK:
            print('Proceed to in-detail setting!')
            sizeSet = fl.radiusdef(int(dlgMultiDis.data[0]))
            distanceSet = fl.distancedef(displaySize, int(dlgMultiDis.data[1]))
            angleSet = fl.angledef(int(dlgMultiDis.data[2]))
            repetition = fl.repeatCount(dlgMultiDis.data[3])
            if (dlgMultiDis.data[4] == 'Yes'):
                hint = True
            else:
                hint = False
            if (dlgMultiDis.data[5] == 'Yes'):
                centering = True
            else:
                centering = False
        else:
            return
    elif (dlg.data[5] == 'Random spawn discrete'):
        dlgRanS.show()
        if dlgRanS.OK:
            print('Proceed to in-detail setting!')
            sizeSet = fl.radiusdef(int(dlgRanS.data[0]))
            distanceSet = fl.distancedef(displaySize, int(dlgRanS.data[1]))
            trial = int(dlgRanS.data[2])
            repetition = fl.repeatCount(dlgRanS.data[3])
            if (dlgRanS.data[4] == 'Yes'):
                hint = True
            else:
                hint = False
        else:
            return

    dlgdefine = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
    dlgdefine.addText('Sizes')
    for i in range(len(sizeSet)):
        dlglabel = 'Size ' + str(i+1)
        dlgdefine.addField(initial=sizeSet[i], label=dlglabel)
    dlgdefine.addText('Distances')
    for i in range(len(distanceSet)):
        dlglabel = 'Distance ' + str(i+1)
        dlgdefine.addField(initial=distanceSet[i], label=dlglabel)
    if (dlg.data[5] == 'Multi-dimensional serial' or dlg.data[5] == 'Multi-dimensional discrete'):
        dlglabel = 'Set angles manually?'
        dlgdefine.addField(initial=False, label=dlglabel)
    dlgdefine.show()
    if dlgdefine.OK:
        # assign value back to sizes and distances
        for i in range(len(sizeSet)):
            sizeSet[i] = dlgdefine.data[i]
        for i in range(len(distanceSet)):
            distanceSet[i] = dlgdefine.data[i+len(sizeSet)]
    else:
        return

    if (dlg.data[5] == 'Multi-dimensional serial' or dlg.data[5] == 'Multi-dimensional discrete'):
        if (dlgdefine.data[len(sizeSet)+len(distanceSet)] == True):
            dlgdefineAngle = gui.Dlg(title="Psychopy Fitts's law test ver 2.0")
            dlgdefineAngle.addText('Angles')
            for i in range(len(angleSet)):
                dlglabel = 'Angle ' + str(i+1)
                dlgdefineAngle.addField(initial=angleSet[i], label=dlglabel)
            dlgdefineAngle.show()
            if dlgdefineAngle.OK:
                # assign value back to angles
                for i in range(len(angleSet)):
                    angleSet[i] = dlgdefineAngle.data[i]
            else:
                return

    # create csv files to store data

    infoFileName = './data/' + \
        dlg.data[0] + '_' + dlg.data[1] + '_' + dlg.data[2] + '_info'
    dataFileName = './data/' + \
        dlg.data[0] + '_' + dlg.data[1] + '_' + dlg.data[2] + '_data'
    posFileName = './data/' + dlg.data[0] + \
        '_' + dlg.data[1] + '_' + dlg.data[2] + '_pos'

    infoFile = open(infoFileName+'.csv', 'a')
    dataFile = open(dataFileName+'.csv', 'a')
    posDataFile = open(posFileName+'.csv', 'a')

    print('The experiment has been set up with following parameters:')
    print('File name: ', dataFileName)
    print('Cursor position file name: ', posFileName)
    print('Test type: ', dlg.data[5])
    print('Size set: ', sizeSet)
    print('Distance set:', distanceSet)
    if (dlg.data[5] == 'Multi-dimensional serial' or dlg.data[5] == 'Multi-dimensional discrete'):
        print('Angle set: ', angleSet)
    if (dlg.data[5] == '2-dimensional discrete' or dlg.data[5] == '2-dimensional serial' or dlg.data[5] == 'Random spawn discrete' or dlg.data[5] == '1-dimensional discrete' or dlg.data[5] == '1-dimensional serial'):
        print('Trials for each condition: ', trial)
    print('Repeat all condition for: ',  repetition)
    if (dlg.data[5] == '2-dimensional discrete' or dlg.data[5] == 'Multi-dimensional discrete'):
        print('Show target hint: ', hint)
        print('Center the cursor for each trial: ', centering)

    # Add experiment info to Data file
    infoFile.write('Subject name/number:' + ',' + str(dlg.data[0]) + '\n')
    infoFile.write('Input Device:' + ',' + str(dlg.data[1]) + '\n')
    infoFile.write('Speed setting:' + ',' + str(dlg.data[2]) + '\n')
    infoFile.write('Display width:' + ',' + str(winWidth) + '\n')
    infoFile.write('Display height:' + ',' + str(winHeight) + '\n')
    infoFile.write('Exp type:' + ',' + str(dlg.data[5]) + '\n')
    if (dlg.data[5] == 'Multi-dimensional serial' or dlg.data[5] == 'Multi-dimensional discrete'):
        infoFile.write('Angle set:' + ',' + str(angleSet)[1:-1] + '\n')
    else:
        infoFile.write('Angle set:' + ',' + 'NaN' + '\n')
    if (dlg.data[5] == '2-dimensional discrete' or dlg.data[5] == '2-dimensional serial' or dlg.data[5] == '1-dimensional discrete' or dlg.data[5] == '1-dimensional serial'):
        infoFile.write('Trials for each condition: ' + ',' + str(trial) + '\n')
    else:
        infoFile.write('Trials for each condition: ' + ',' + 'NaN' + '\n')
    if (dlg.data[5] == '1-dimensional discrete' or dlg.data[5] == '1-dimensional serial'):
        infoFile.write('Direction: ' + ',' + str(direction) + '\n')
    else:
        infoFile.write('Direction: ' + ',' + 'NaN' + '\n')
    infoFile.write('Repeat all condition for:' +
                   ',' + str(repetition - 1) + '\n')
    if (dlg.data[5] == '2-dimensional discrete' or dlg.data[5] == 'Multi-dimensional discrete' or dlg.data[5] == '1-dimensional discrete'):
        infoFile.write('Show target hint:' + ',' + str(hint) + '\n')
        infoFile.write('Center the cursor for each trial:' +
                       ',' + str(centering) + '\n')
    else:
        infoFile.write('Show target hint:' + ',' + 'NaN' + '\n')
        infoFile.write('Center the cursor for each trial:' +
                       ',' + 'NaN' + '\n')
    infoFile.write('Size set:' + ',' + str(sizeSet)[1:-1] + '\n')
    infoFile.write('Distance set: ' + ',' + str(distanceSet)[1:-1] + '\n')

    dataFile.write('Index of difficulty (bits)' + ',' + 'Response time (ms)' + ',' + 'Target size (px)' + ',' + 'Target distance (px)' +
                   ',' + 'Start time (s)' + ',' + 'End time (s)' + ',' + 'Target position X (px)' + ',' + 'Target position Y (px)\n')

    # Define the test window
    if (dlg.data[5] == 'Random spawn discrete' or dlg.data[5] == '1-dimensional discrete' or dlg.data[5] == '1-dimensional serial'):
        win = visual.Window(size=(winWidth, winHeight), allowGUI=False,
                            monitor='None', units='pix', fullscr=full, color=[255, 255, 255], screen=screen)
    else:
        win = visual.Window(size=(displaySize, displaySize), allowGUI=False,
                            monitor='None', units='pix', fullscr=full, screen=screen)
    print("windows defined")
    win.setColor('white')
    win.flip()

    # Define text stimulus
    intro_MultiDiscrete = visual.TextStim(
        win, text="Click on the blue ball, and click on the red ball as fast and accurate as possible", color='black')
    intro_MultiSerial = visual.TextStim(
        win, text="Click on the red ball as fast and accurate as possible", color='black')
    intro_2DDiscrete = visual.TextStim(
        win, text="Click on the blue bar, and click on the red bar as fast and accurate as possible", color='black')
    intro_2DSerial = visual.TextStim(
        win, text="Click on the red bar as fast and accurate as possible", color='black')
    intro_1DDiscrete = visual.TextStim(
        win, text="Click on the blue bar, and click on the red bar as fast and accurate as possible", color='black')
    intro_1DSerial = visual.TextStim(
        win, text="Click on the red bar as fast and accurate as possible", color='black')
    intro_RandomSpawn = visual.TextStim(
        win, text="Click on the blue ball, and click on the red ball as fast and accurate as possible", color='black')

    ending = visual.TextStim(
        win, text="The section ends here, please inform the researcher.", color='black')

    print("Intro prompt defined")

    # Intro
    if (dlg.data[5] == '2-dimensional serial'):
        intro_2DSerial.draw()
    elif (dlg.data[5] == '2-dimensional discrete'):
        intro_2DDiscrete.draw()
    elif (dlg.data[5] == '1-dimensional serial'):
        intro_1DSerial.draw()
    elif (dlg.data[5] == '1-dimensional discrete'):
        intro_1DDiscrete.draw()
    elif (dlg.data[5] == 'Multi-dimensional serial'):
        intro_MultiSerial.draw()
    elif (dlg.data[5] == 'Multi-dimensional discrete'):
        intro_MultiDiscrete.draw()
    else:
        intro_RandomSpawn.draw()

    win.flip()
    print("Intro showed")
    event.waitKeys()
    win.flip()

    # Send test markers to test communication
    for _ in range(5):
        outlet.push_sample(markers['start'])
        core.wait(0.5)
    print("Test marker sent...")

    for _ in range(repetition):
        if (dlg.data[5] == 'Multi-dimensional discrete'):
            outlet.push_sample(markers['sectionstart'])
            fl.multiDiscrete(win, markers, sizeSet, distanceSet, angleSet,
                             outlet, dataFile, posDataFile, hint, centering)
            outlet.push_sample(markers['sectionend'])
        elif (dlg.data[5] == 'Multi-dimensional serial'):
            outlet.push_sample(markers['sectionstart'])
            fl.multiSerial(win, markers, sizeSet, distanceSet,
                           angleSet, outlet, dataFile, posDataFile)
            outlet.push_sample(markers['sectionend'])
        elif (dlg.data[5] == '1-dimensional discrete'):
            outlet.push_sample(markers['sectionstart'])
            fl.oneDiscrete(win, winWidth, winHeight, markers, sizeSet, distanceSet,
                           direction, trial, outlet, dataFile, posDataFile, hint, centering)
            outlet.push_sample(markers['sectionend'])
        elif (dlg.data[5] == '1-dimensional serial'):
            outlet.push_sample(markers['sectionstart'])
            fl.oneSerial(win, winWidth, winHeight, markers, sizeSet,
                         distanceSet, direction, trial, outlet, dataFile, posDataFile)
            outlet.push_sample(markers['sectionend'])
        elif (dlg.data[5] == '2-dimensional discrete'):
            outlet.push_sample(markers['sectionstart'])
            fl.twoDiscrete(win, winWidth, winHeight, markers, sizeSet, distanceSet,
                           trial, outlet, dataFile, posDataFile, hint, centering)
            outlet.push_sample(markers['sectionend'])
        elif (dlg.data[5] == '2-dimensional serial'):
            outlet.push_sample(markers['sectionstart'])
            fl.twoSerial(win, winWidth, winHeight, markers, sizeSet,
                         distanceSet, trial, outlet, dataFile, posDataFile)
            outlet.push_sample(markers['sectionend'])
        else:
            outlet.push_sample(markers['sectionstart'])
            fl.randomSpawn(win, winWidth, winHeight, markers, sizeSet,
                           distanceSet, trial, outlet, dataFile, posDataFile, hint)
            outlet.push_sample(markers['sectionend'])

    # Send ending markers through LSL
    for _ in range(5):
        outlet.push_sample(markers['end'])
        core.wait(0.5)

    # Ending text
    ending.draw()
    win.flip()
    print("The test ends here!")
    event.waitKeys()

    # Exit at the end of experiment
    posDataFile.write('\n')
    posDataFile.close()
    dataFile.write('\n')
    dataFile.close()
    win.close()
    core.quit()


if __name__ == "__main__":
    main()
