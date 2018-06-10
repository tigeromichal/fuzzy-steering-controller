# fuzzy-steering-controller
Simple fuzzy steering controller simulation written in Python

Simulation contains of 4 elements - a road with two lanes, cars A and B going in the same direction, and car C going in the opposite direction. The problem for the given algorithm to solve is to steer car A acceleration in such a way, so it safely overtakes car B before reaching the end of the road, without crashing to any of the cars B and C.

Python packages needed:
* pygame (optional)

Intial state of the simulation stored in data/initialState.txt:
`A 0 1 16`
`B 100 1 20`
`C 1700 0 -16`
where each line is of format:
`car_name initial_position initial_lane initial_speed`

main.py CLI arguments:
* initial state file name: path to initial state file
* output file name: path to output data file
* random initial state: True / False - specifies. whether initial state of the simulation will be generated automatically or loaded from initialState.txt file
* random acc: True / False - specifies, whether cars B and C can, in each cycle, with probability of 10%, randomly change their speed by +/- 5m/s
* number of steps: integer - number of tests to perform
* fps: integer - number of cycles / frames in one second