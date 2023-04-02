import random
import math
import pylsl as lsl
import tkinter as tk
from psychopy import core, visual, event


def multiSerial(win, markers, sizeSet, distanceSet, angleSet, outlet, dataFile, posDataFile):

    mouse = event.Mouse()
    mousePos = tk.Tk()
    # Task randomization based on conditions
    sizeXdistance = []
    for i in range(len(distanceSet)):
        for j in range(len(sizeSet)):
            sizeXdistance.append([sizeSet[j], distanceSet[i]])
    random.shuffle(sizeXdistance)
    print("sizeXdistance", sizeXdistance)

    for k in range(len(sizeXdistance)):
        outlet.push_sample(markers['conditionstart'])
        randomStart = random.randint(0, len(angleSet))
        newAngleSet = angleSeq(angleSet, randomStart)
        firstClick = True
        siz = sizeXdistance[k][0]
        dis = sizeXdistance[k][1]
        stimGhost = []
        for i in range(len(angleSet)):
            posXg = math.ceil(0 - dis*math.cos(math.radians(angleSet[i])))
            posYg = math.ceil(0 - dis*math.sin(math.radians(angleSet[i])))
            stimGhost.append(visual.Circle(win, units='pix', fillColor='gray', pos=(
                posXg, posYg), radius=siz))
            print("passed")

        for i in range(len(newAngleSet)):
            posX = math.ceil(0 - dis*math.cos(math.radians(newAngleSet[i])))
            posY = math.ceil(0 - dis*math.sin(math.radians(newAngleSet[i])))

            marker = [siz, dis, posX, posY]
            print(marker)

            stimFirst = visual.Circle(win, units='pix', fillColor='red', pos=(
                posX, posY), radius=siz)

            for i in range(len(angleSet)):
                stimGhost[i].draw()
            stimFirst.draw()
            win.flip()
            startTime = core.getTime()
            posDataFile.write('Index of Difficulty' + ',' + 'Size (px)' + ',' + 'Distance (px)' +
                              ',' + 'Target Position X (px)' + ',' + 'Target Position Y (px)' + '\n')
            posDataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(siz) +
                              ',' + str(dis) + ',' + str(posX) + ',' + str(posY) + '\n')
            posDataFile.write('Timestamp (s)' + ',' +
                              'Position X (px)' + ',' + 'Position Y (px)\n')
            prepos = [0, 0]
            while True:
                if 'escape' in event.getKeys():  # Exit if user presses escape.
                    core.quit()
                if firstClick == False:
                    outlet.push_sample(markers['clickstart'])
                    pos = mousePos.winfo_pointerxy()
                    if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                        posDataFile.write(
                            str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) + '\n')
                        prepos = pos
                        # print (pos)
                    # posDataFile.write(str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) +'\n')

                if mouse.isPressedIn(stimFirst):
                    if firstClick:
                        startTime = core.getTime()
                        firstClick = False
                    outlet.push_sample(markers['clickstart'])
                    endTime = core.getTime()
                    break
            rt = int(round((endTime - startTime)*1000))
            dataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(rt) + ',' + str(siz) + ',' + str(
                dis) + ',' + str(startTime) + ',' + str(endTime) + ',' + str(posX) + ',' + str(posY) + '\n')
            print(rt)
        print('Condition ended')
        outlet.push_sample(markers['conditionend'])
        win.flip()


def multiDiscrete(win, markers, sizeSet, distanceSet, angleSet, outlet, dataFile, posDataFile, hint, centering):

    stimFirst = visual.Circle(
        win, units='pix', fillColor='blue', pos=(0, 0), radius=10)
    mouse = event.Mouse()
    mousePos = tk.Tk()

    # Task randomization based on conditions
    sizeXdistance = []
    for i in range(len(distanceSet)):
        for j in range(len(sizeSet)):
            sizeXdistance.append([sizeSet[j], distanceSet[i]])
    random.shuffle(sizeXdistance)
    print(sizeXdistance)

    random.shuffle(angleSet)
    print(angleSet)

    for k in range(len(sizeXdistance)):
        outlet.push_sample(markers['conditionstart'])
        for i in range(len(angleSet)):
            siz = sizeXdistance[k][0]
            dis = sizeXdistance[k][1]
            posX = math.ceil(0 - dis*math.cos(math.radians(angleSet[i])))
            posY = math.ceil(0 - dis*math.sin(math.radians(angleSet[i])))
            marker = [siz, dis, posX, posY]
            print(marker)
            stimSecondGhost = visual.Circle(
                win, units='pix', fillColor='gray', pos=(posX, posY), radius=siz)
            if (hint):
                stimSecondGhost.draw()
            stimFirst.draw()
            win.flip()
            if (centering):
                mouse = event.Mouse(newPos=[0, 0])
            posDataFile.write('Index of Difficulty' + ',' + 'Size (px)' + ',' + 'Distance (px)' +
                              ',' + 'Target Position X (px)' + ',' + 'Target Position Y (px)' + '\n')
            posDataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(siz) +
                              ',' + str(dis) + ',' + str(posX) + ',' + str(posY) + '\n')
            posDataFile.write('Timestamp (s)' + ',' +
                              'Position X (px)' + ',' + 'Position Y (px)' + '\n')
            prepos = [0, 0]
            while True:
                if 'escape' in event.getKeys():  # Exit if user presses escape.
                    core.quit()
                if mouse.isPressedIn(stimFirst):
                    outlet.push_sample(markers['clickstart'])
                    startTime = core.getTime()
                    # pos = mousePos.winfo_pointerxy()
                    # if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                    #     posDataFile.write(str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) +'\n')
                    #     prepos = pos
                    break
            stimSecond = visual.Circle(win, units='pix', fillColor='red', pos=(
                posX, posY), radius=siz)
            stimSecond.draw()
            win.flip()
            while True:
                if 'escape' in event.getKeys():  # Exit if user presses escape.
                    core.quit()
                pos = mousePos.winfo_pointerxy()
                if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                    posDataFile.write(
                        str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) + '\n')
                    prepos = pos
                if mouse.isPressedIn(stimSecond):
                    outlet.push_sample(markers['clickend'])
                    endTime = core.getTime()
                    break
            rt = int(round((endTime - startTime)*1000))
            dataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(rt) + ',' + str(siz) + ',' + str(
                dis) + ',' + str(startTime) + ',' + str(endTime) + ',' + str(posX) + ',' + str(posY) + '\n')
            print(rt)
        random.shuffle(angleSet)
        print('Block ended')
        outlet.push_sample(markers['conditionend'])
        win.flip()


def twoSerial(win, winWidth, winHeight, markers, sizeSet, distanceSet, repetition, outlet, dataFile, posDataFile):
    mouse = event.Mouse()
    mousePos = tk.Tk()

    # Task randomization based on conditions
    sizeXdistance = []
    for i in range(len(distanceSet)):
        for j in range(len(sizeSet)):
            sizeXdistance.append([sizeSet[j], distanceSet[i]])
    random.shuffle(sizeXdistance)
    print(sizeXdistance)

    for k in range(len(sizeXdistance)):
        outlet.push_sample(markers['conditionstart'])
        firstClick = True
        siz = sizeXdistance[k][0]
        dis = sizeXdistance[k][1]
        flip = True

        for x in range(2):
            for i in range(repetition):
                if x % 2:
                    if flip:
                        stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                            -1*dis, 0), width=siz, height=winHeight)
                        stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                            dis, 0), width=siz, height=winHeight)
                        flip = False
                    else:
                        stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                            dis, 0), width=siz, height=winHeight)
                        stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                            -1*dis, 0), width=siz, height=winHeight)
                        flip = True
                else:
                    if flip:
                        stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                            0, -1*dis), width=winWidth, height=siz)
                        stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                            0, dis), width=winWidth, height=siz)
                        flip = False
                    else:
                        stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                            0, dis), width=winWidth, height=siz)
                        stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                            0, -1*dis), width=winWidth, height=siz)
                        flip = True
                stimGhost.draw()
                stimulus.draw()
                win.flip()
                startTime = core.getTime()
                posDataFile.write('Index of Difficulty' + ',' +
                                  'Size (px)' + ',' + 'Distance (px)' + '\n')
                posDataFile.write(str(math.log((2*dis/siz), 2)) +
                                  ',' + str(siz) + ',' + str(dis) + '\n')
                posDataFile.write(
                    'Timestamp (s)' + ',' + 'Position X (px)' + ',' + 'Position Y (px)' + '\n')
                prepos = [0, 0]
                while True:
                    if 'escape' in event.getKeys():  # Exit if user presses escape.
                        core.quit()
                    if firstClick == False:
                        outlet.push_sample(markers['clickstart'])
                        pos = mousePos.winfo_pointerxy()
                        if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                            posDataFile.write(
                                str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) + '\n')
                            prepos = pos
                        # print (pos)
                    if mouse.isPressedIn(stimulus):
                        if firstClick:
                            startTime = core.getTime()
                            firstClick = False
                        outlet.push_sample(markers['clickstart'])
                        endTime = core.getTime()
                        break
                rt = int(round((endTime - startTime)*1000))
                dataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(rt) + ',' + str(
                    siz) + ',' + str(dis) + ',' + str(startTime) + ',' + str(endTime) + '\n')
                print(rt)
            outlet.push_sample(markers['directionchange'])
        outlet.push_sample(markers['conditionend'])


def twoDiscrete(win, winWidth, winHeight, markers, sizeSet, distanceSet, repetition, outlet, dataFile, posDataFile, hint, centering):
    mouse = event.Mouse()
    mousePos = tk.Tk()

    # Task randomization based on conditions
    sizeXdistance = []
    for i in range(len(distanceSet)):
        for j in range(len(sizeSet)):
            sizeXdistance.append([sizeSet[j], distanceSet[i]])
    random.shuffle(sizeXdistance)
    print(sizeXdistance)

    for k in range(len(sizeXdistance)):
        siz = sizeXdistance[k][0]
        dis = sizeXdistance[k][1]
        flip = True

        for x in range(2):
            for i in range(repetition):
                if x % 2:
                    stimFirst = visual.Rect(win, units='pix', fillColor='blue', pos=(
                        0, 0), width=20, height=winHeight)
                    if flip:
                        stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                            dis, 0), width=siz, height=winHeight)
                        stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                            dis, 0), width=siz, height=winHeight)
                        flip = False
                    else:
                        stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                            -1*dis, 0), width=siz, height=winHeight)
                        stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                            -1*dis, 0), width=siz, height=winHeight)
                        flip = True
                else:
                    stimFirst = visual.Rect(win, units='pix', fillColor='blue', pos=(
                        0, 0), width=winWidth, height=20)
                    if flip:
                        stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                            0, dis), width=winWidth, height=siz)
                        stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                            0, dis), width=winWidth, height=siz)
                        flip = False
                    else:
                        stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                            0, -1*dis), width=winWidth, height=siz)
                        stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                            0, -1*dis), width=winWidth, height=siz)
                        flip = True
                if (hint):
                    stimGhost.draw()
                stimFirst.draw()
                win.flip()
                posDataFile.write('Index of Difficulty' + ',' +
                                  'Size (px)' + ',' + 'Distance (px)' + '\n')
                posDataFile.write(str(math.log((2*dis/siz), 2)) +
                                  ',' + str(siz) + ',' + str(dis) + '\n')
                posDataFile.write(
                    'Timestamp (s)' + ',' + 'Position X (px)' + ',' + 'Position Y (px)' + '\n')
                prepos = [0, 0]
                if (centering):
                    mouse = event.Mouse(newPos=[0, 0])
                while True:
                    if 'escape' in event.getKeys():  # Exit if user presses escape.
                        core.quit()
                    if mouse.isPressedIn(stimFirst):
                        outlet.push_sample(markers['clickstart'])
                        startTime = core.getTime()
                        # pos = mousePos.winfo_pointerxy()
                        # if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                        #     posDataFile.write(str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) +'\n')
                        #     prepos = pos
                        break
                stimulus.draw()
                win.flip()
                while True:
                    if 'escape' in event.getKeys():  # Exit if user presses escape.
                        core.quit()
                    pos = mousePos.winfo_pointerxy()
                    if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                        posDataFile.write(
                            str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) + '\n')
                        prepos = pos
                    if mouse.isPressedIn(stimulus):
                        outlet.push_sample(markers['clickend'])
                        endTime = core.getTime()
                        break
                rt = int(round((endTime - startTime)*1000))
                dataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(rt) + ',' + str(
                    siz) + ',' + str(dis) + ',' + str(startTime) + ',' + str(endTime) + '\n')
                print(rt)
            outlet.push_sample(markers['directionchange'])
        outlet.push_sample(markers['conditionend'])


def oneSerial(win, winWidth, winHeight, markers, sizeSet, distanceSet, direction, repetition, outlet, dataFile, posDataFile):
    mouse = event.Mouse()
    mousePos = tk.Tk()

    # Task randomization based on conditions
    sizeXdistance = []
    for i in range(len(distanceSet)):
        for j in range(len(sizeSet)):
            sizeXdistance.append([sizeSet[j], distanceSet[i]])
    random.shuffle(sizeXdistance)
    print(sizeXdistance)

    for k in range(len(sizeXdistance)):
        outlet.push_sample(markers['conditionstart'])
        firstClick = True
        siz = sizeXdistance[k][0]
        dis = sizeXdistance[k][1]
        flip = True

        for i in range(repetition):
            if direction == 'Horizontal':
                if flip:
                    stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                        -1*dis, 0), width=siz, height=winHeight)
                    stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                        dis, 0), width=siz, height=winHeight)
                    flip = False
                else:
                    stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                        dis, 0), width=siz, height=winHeight)
                    stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                        -1*dis, 0), width=siz, height=winHeight)
                    flip = True
            else:
                if flip:
                    stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                        0, -1*dis), width=winWidth, height=siz)
                    stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                        0, dis), width=winWidth, height=siz)
                    flip = False
                else:
                    stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                        0, dis), width=winWidth, height=siz)
                    stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                        0, -1*dis), width=winWidth, height=siz)
                    flip = True
            stimGhost.draw()
            stimulus.draw()
            win.flip()
            startTime = core.getTime()
            posDataFile.write('Index of Difficulty' + ',' +
                              'Size (px)' + ',' + 'Distance (px)' + '\n')
            posDataFile.write(str(math.log((2*dis/siz), 2)) +
                              ',' + str(siz) + ',' + str(dis) + '\n')
            posDataFile.write('Timestamp (s)' + ',' +
                              'Position X (px)' + ',' + 'Position Y (px)' + '\n')
            prepos = [0, 0]
            while True:
                if 'escape' in event.getKeys():  # Exit if user presses escape.
                    core.quit()
                if firstClick == False:
                    pos = mousePos.winfo_pointerxy()
                    if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                        posDataFile.write(
                            str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) + '\n')
                        prepos = pos

                    outlet.push_sample(markers['clickstart'])
                    # print (pos)
                if mouse.isPressedIn(stimulus):
                    if firstClick:
                        startTime = core.getTime()
                        firstClick = False
                    outlet.push_sample(markers['clickstart'])
                    endTime = core.getTime()
                    break
            rt = int(round((endTime - startTime)*1000))
            dataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(rt) + ',' + str(
                siz) + ',' + str(dis) + ',' + str(startTime) + ',' + str(endTime) + '\n')
            print(rt)
        outlet.push_sample(markers['conditionend'])


def oneDiscrete(win, winWidth, winHeight, markers, sizeSet, distanceSet, direction, repetition, outlet, dataFile, posDataFile, hint, centering):
    mouse = event.Mouse()
    mousePos = tk.Tk()

    # Task randomization based on conditions
    sizeXdistance = []
    for i in range(len(distanceSet)):
        for j in range(len(sizeSet)):
            sizeXdistance.append([sizeSet[j], distanceSet[i]])
    random.shuffle(sizeXdistance)
    print(sizeXdistance)

    for k in range(len(sizeXdistance)):
        siz = sizeXdistance[k][0]
        dis = sizeXdistance[k][1]
        flip = True

        for i in range(repetition):
            if direction == 'Horizontal':
                stimFirst = visual.Rect(win, units='pix', fillColor='blue', pos=(
                    0, 0), width=20, height=winHeight)
                if flip:
                    stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                        dis, 0), width=siz, height=winHeight)
                    stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                        dis, 0), width=siz, height=winHeight)
                    flip = False
                else:
                    stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                        -1*dis, 0), width=siz, height=winHeight)
                    stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                        -1*dis, 0), width=siz, height=winHeight)
                    flip = True
            else:
                stimFirst = visual.Rect(win, units='pix', fillColor='blue', pos=(
                    0, 0), width=winWidth, height=20)
                if flip:
                    stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                        0, dis), width=winWidth, height=siz)
                    stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                        0, dis), width=winWidth, height=siz)
                    flip = False
                else:
                    stimGhost = visual.Rect(win, units='pix', fillColor='gray', pos=(
                        0, -1*dis), width=winWidth, height=siz)
                    stimulus = visual.Rect(win, units='pix', fillColor='red', pos=(
                        0, -1*dis), width=winWidth, height=siz)
                    flip = True
            if (hint):
                stimGhost.draw()
            stimFirst.draw()
            win.flip()
            posDataFile.write('Index of Difficulty' + ',' +
                              'Size (px)' + ',' + 'Distance (px)' + '\n')
            posDataFile.write(str(math.log((2*dis/siz), 2)) +
                              ',' + str(siz) + ',' + str(dis) + '\n')
            posDataFile.write('Timestamp (s)' + ',' +
                              'Position X (px)' + ',' + 'Position Y (px)' + '\n')
            prepos = [0, 0]
            if (centering):
                mouse = event.Mouse(newPos=[0, 0])
            while True:
                if 'escape' in event.getKeys():  # Exit if user presses escape.
                    core.quit()
                if mouse.isPressedIn(stimFirst):
                    outlet.push_sample(markers['clickstart'])
                    startTime = core.getTime()
                    # pos = mousePos.winfo_pointerxy()
                    # if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                    #     posDataFile.write(str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) +'\n')
                    #     prepos = pos
                    break
            stimulus.draw()
            win.flip()
            while True:
                if 'escape' in event.getKeys():  # Exit if user presses escape.
                    core.quit()
                pos = mousePos.winfo_pointerxy()
                if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                    posDataFile.write(
                        str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) + '\n')
                    prepos = pos
                if mouse.isPressedIn(stimulus):
                    outlet.push_sample(markers['clickend'])
                    endTime = core.getTime()
                    break
            rt = int(round((endTime - startTime)*1000))
            dataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(rt) + ',' + str(
                siz) + ',' + str(dis) + ',' + str(startTime) + ',' + str(endTime) + '\n')
            print(rt)
        outlet.push_sample(markers['conditionend'])


def randomSpawn(win, winWidth, winHeight, markers, sizeSet, distanceSet, repetition, outlet, dataFile, posDataFile, hint):
    mouse = event.Mouse()
    mousePos = tk.Tk()
    # Task randomization based on conditions
    sizeXdistance = []
    for i in range(len(distanceSet)):
        for j in range(len(sizeSet)):
            sizeXdistance.append([sizeSet[j], distanceSet[i]])
    random.shuffle(sizeXdistance)
    print(sizeXdistance)

    stimDis = []
    stimSiz = []
    stimPosX = []
    stimPosY = []
    stimPosXg = []
    stimPosYg = []
    stimAngle = []
    cornerXset = []
    cornerYset = []
    for i in range(repetition):
        for k in range(len(sizeXdistance)):
            siz = sizeXdistance[k][0]
            dis = sizeXdistance[k][1]

            # Pick a spaw location
            posX, posY, posXg, posYg, angle, cornerX, cornerY = randomSpaw(
                dis, winWidth, winHeight)
            stimSiz.append(siz)
            stimDis.append(dis)
            stimPosX.append(posX)
            stimPosY.append(posY)
            stimPosXg.append(posXg)
            stimPosYg.append(posYg)
            stimAngle.append(angle)
            cornerXset.append(cornerX)
            cornerYset.append(cornerY)

    randomIndex = random.sample(range(0, len(stimPosX)), len(stimPosX))

    for i in range(len(sizeXdistance)*repetition):
        siz = stimSiz[randomIndex[i]]
        dis = stimDis[randomIndex[i]]
        posX = stimPosX[randomIndex[i]]
        posY = stimPosY[randomIndex[i]]
        posXg = stimPosXg[randomIndex[i]]
        posYg = stimPosYg[randomIndex[i]]

        stimFirst = visual.Circle(win, units='pix', fillColor='blue', pos=(
            posX, posY), radius=10)
        stimSecondGhost = visual.Circle(win, units='pix', fillColor='gray', pos=(
            posXg, posYg), radius=siz)
        if (hint):
            stimSecondGhost.draw()
        stimFirst.draw()
        win.flip()
        posDataFile.write('Index of Difficulty' + ',' + 'Size (px)' + ',' + 'Distance (px)' +
                          ',' + 'Target Position X (px)' + ',' + 'Target Position Y (px)' + '\n')
        posDataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(siz) +
                          ',' + str(dis) + ',' + str(posX) + ',' + str(posY) + '\n')
        posDataFile.write('Timestamp (s)' + ',' +
                          'Position X (px)' + ',' + 'Position Y (px)' + '\n')
        print(siz, dis, posX, posY, posXg, posYg,
              stimAngle[randomIndex[i]], cornerXset[randomIndex[i]], cornerYset[randomIndex[i]])
        prepos = [0, 0]
        while True:
            if 'escape' in event.getKeys():  # Exit if user presses escape.
                core.quit()
            if mouse.isPressedIn(stimFirst):
                outlet.push_sample(markers['clickstart'])
                startTime = core.getTime()
                # pos = mousePos.winfo_pointerxy()
                # if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                #     posDataFile.write(str(core.getTime()) + ',' + str(pos[0]) + ',' + str(pos[1]) +'\n')
                #     prepos = pos
                break
        stimSecond = visual.Circle(win, units='pix', fillColor='red', pos=(
            posXg, posYg), radius=siz)
        stimSecond.draw()
        win.flip()
        while True:
            if 'escape' in event.getKeys():  # Exit if user presses escape.
                core.quit()
            pos = mousePos.winfo_pointerxy()
            if (pos[0] != prepos[0] or pos[1] != prepos[1]):
                posDataFile.write(str(core.getTime()) + ',' +
                                  str(pos[0]) + ',' + str(pos[1]) + '\n')
                prepos = pos

            if mouse.isPressedIn(stimSecond):
                outlet.push_sample(markers['clickend'])
                endTime = core.getTime()
                break
        rt = int(round((endTime - startTime)*1000))
        dataFile.write(str(math.log((2*dis/siz), 2)) + ',' + str(rt) + ',' + str(siz) + ',' + str(
            dis) + ',' + str(startTime) + ',' + str(endTime) + ',' + str(posX) + ',' + str(posY) + '\n')
        print(rt)


def angledef(count):
    angleSet = []
    for i in range(count):
        angle = int(round(360/count*(i+1)))
        angleSet.append(angle)
    return angleSet


def distancedef(height, count):
    distanceSet = []
    height = height/2 - 50
    for i in range(count):
        distance = int(round((height/(count))*(i+1)))
        distanceSet.append(distance)
    return distanceSet


def sizedef(count):
    if (count == 1):
        sizeSet = [40]
    elif (count == 2):
        sizeSet = [20, 60]
    elif (count == 3):
        sizeSet = [20, 40, 60]
    elif (count == 4):
        sizeSet = [15, 30, 45, 60]
    elif (count == 5):
        sizeSet = [15, 25, 35, 45, 55]
    elif (count == 6):
        sizeSet = [10, 20, 30, 40, 50, 60]
    elif (count == 7):
        sizeSet = [10, 20, 30, 40, 50, 60, 70]
    return sizeSet


def radiusdef(count):
    if (count == 1):
        sizeSet = [20]
    elif (count == 2):
        sizeSet = [10, 30]
    elif (count == 3):
        sizeSet = [10, 20, 30]
    elif (count == 4):
        sizeSet = [10, 20, 30, 40]
    elif (count == 5):
        sizeSet = [10, 15, 20, 25, 30]
    elif (count == 6):
        sizeSet = [10, 15, 20, 25, 30, 35]
    elif (count == 7):
        sizeSet = [10, 15, 20, 25, 30, 35, 40]
    return sizeSet


def angleSeq(angle, start):
    angleSet = []
    increment = int(len(angle)/2)
    x = start % len(angle)
    for _ in range(len(angle)):
        angleSet.append(angle[x])
        x = (x + increment) % len(angle)
    angleSet.append(angle[start % len(angle)])
    return angleSet


def repeatCount(repeat):
    if (repeat == 'No repeat'):
        count = 1
    else:
        count = int(repeat) + 1
    return count


def randomSpaw(dis, winWidth, winHeight):
    randomX = random.randint((50-winWidth/2), (winWidth/2-50))
    randomY = random.randint((50-winHeight/2), (winHeight/2-50))
    if (randomX >= 0):
        if ((randomX + dis) > (winWidth/2-90)):
            cornerX = 1
        else:
            cornerX = 0
    else:
        if ((randomX - dis) < -(winWidth/2-90)):
            cornerX = -1
        else:
            cornerX = 0

    if (randomY >= 0):
        if ((randomY + dis) > (winHeight/2-90)):
            cornerY = 1
        else:
            cornerY = 0
    else:
        if ((randomY - dis) < -(winHeight/2-90)):
            cornerY = -1
        else:
            cornerY = 0

    if (cornerX == 1 and cornerY == -1):
        angle = random.randint(90, 180)
    elif (cornerX == -1 and cornerY == -1):
        angle = random.randint(0, 90)
    elif (cornerX == 1 and cornerY == 1):
        angle = random.randint(180, 270)
    elif (cornerX == -1 and cornerY == 1):
        angle = random.randint(270, 360)
    elif (cornerX == 1 and cornerY == 0):
        angle = random.randint(90, 270)
    elif (cornerX == -1 and cornerY == 0):
        angle = random.randint(-90, 90)
    elif (cornerX == 0 and cornerY == 1):
        angle = random.randint(180, 360)
    elif (cornerX == 0 and cornerY == -1):
        angle = random.randint(0, 180)
    else:
        angle = random.randint(0, 360)

    posXg = math.ceil(randomX+dis*math.cos(math.radians(angle)))
    posYg = math.ceil(randomY+dis*math.sin(math.radians(angle)))

    return (randomX, randomY, posXg, posYg, angle, cornerX, cornerY)
