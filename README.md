# Psychopy Fitts's Law testing program #
LabStreamingLayer (LSL) embedded which will send markers to any LabStreamingLayer enabled devices for time and event synchronization.

**Features**
- Supported test paradigms:
    - Multi-dimensional discrete
    - Multi-dimensional serial
    - 2-dimensional discrete
    - 2-dimensional serial
    - 1-dimensional discrete
    - 1-dimensional serial
    - Random spawn discrete
- Customizable parameters (can be further modified in the code):
    - Up to 8 size variations
    - Up to 8 distance variations
    - From 7 to up to 25 angle variations (for the multi-dimensional test only)
    - How many trials per condition (for the 1 and 2-dimensional test only)
    - Select the target direction (for the 1-dimensional test only)
    - Repeat all conditions for up to ten times.
- The sizes, distances, and angles can be set manually set or have the program calculates them automatically.
- For discrete mode, you can decide whether you want to show a hint for the next target location or whether the cursor should be centered for each trial.
- The response time for each trial will be exported as a .csv together with trial information and the index of difficulty (ID).
- The cursor position can be tracked in real-time and logged as a .csv file with timestamps

**To Use**
- You will need to have PsychoPy 3 installed, additionally, you will need to pip install pylsl for data streaming
- Run "runFittsLaw.py" through Psychopy or CMD, LSL stream will be created and become avaiable when the dialogue box shows up
- The field subject name/number, Input device, and speed setting are for putting in participant and test condition info. The three fields will be concatenated with _ to become the name of the data files. If no info is provided, the file name will be ___. The data files will be appended if you assigned the same filename. 
- There are many other options for you to set. Please review each one carefully before proceed

**Notes**
- Serial: The subject can keep clicking at the red target
- Discrete: The subject will have to click at the blue target at the center each time before clicking at the red target
- Hint: In discrete mode, the subject can see where the next target is
- Center the cursor for each trial: In discrete mode, the mouse cursor will be repositioned to the center after each click