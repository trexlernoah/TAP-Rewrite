What needs to be done:
[X] tweak the reaction timer to work when the user releases the space bar

- some sort of format for saving data to a .dat file (not a word doc, a .dat file - .dat files can be opened in Word) - Dictionary? I think before I was planning to write each value to the experiments.txt file and seperate them with dashes - ex: trial-1:<Win/Loss value>-<Shock>-<Duration>-<Reaction time> - It might be easier to just append this to a .dat file as the experiment is being run.
  [X] combine the reaction timer and the shock meter selection into one
- collect the data from the two and store it somewhere
- if shock button is held for longer than a certain amount of time (7 seconds for the moment), stop the shock and display a message
- Shock dial should only show for as long as button is being pressed, record how long button is being pressed
- if 4 seconds elapse without the user pressing the space bar, prompt them to release the space bar
- if the user releases the space bar too soon, have an error that tells them to press the space bar
- have then release the space pbar within 1 second - valid response, task advances. Longer than 1 second is an error - held space bar for too long
- remind user to press shock button if they have not after some amount of time

[X] Initialize experiment config file
[X] Function to autogenerate file
[X] Function to enter info from window

[X] Set pain threshold
[X] Function to send shock
[X] Function to send out pulse
[X] Function for ramping up the intensity over time
[X] Function to collect data
[X] Function to write/modify data to and from config file

[X] In Number of Trials and Shock Duration, check to make sure input is only numbers

# Worry about this later

[ ] Fix the filename being set to "experiment" in every creation - have it be set to subject ID as soon as possible
[ ] Program functions for the following:
[ ] Create
[ ] Instruction
[ ] Experiment
[ ] Profile Setup # Worry about this later
[ ] Enable RCAP box
[X] Setup Profile Parameters
[X] Generate trial fields with for loop depending on number of trials
[ ] Experiment
[ ] Experiment Components/building blocks/whatever
[X] Fullscreen window
[X] Updating text depending on input/lack thereof
[ ] Data being saved
[X] Getting keyboard input for 0-9 keys for shock
[X] Getting reaction time for spacebar
[X] ~~Rectangles~~ Circles that update to show which option has been selected
[X] Speedometer/gauge that shows relative shock value
[X] Improve the performance of this somehow - main issue is that it draws so many small individual lines instead of just filling in the area with color, so the program needs to compute and draw each line
[ ] Combine everything into working demo
[X] Open Experiment (return data to some ledger (?))
[ ] Edit Current
[ ] Instruction
[ ] Experiment
[X] Subjct Threshold
[X] Subject ID
[X] Set Lower Level
[X] Set Higher Level
[X] Ok (return data to some ledger (?))
[ ] Run
[ ] Practice
[ ] Official

send software list for remote access
