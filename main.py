import argparse

from Simulator import Simulator

parser = argparse.ArgumentParser()

parser.add_argument('--isfp', action='store', default="data/initialState.txt", dest='initial_state_file_name',
                    help='Initial state file path')
parser.add_argument('--is', action='store', default=True, dest='random_initial_state',
                    help='Allow random initial state')
parser.add_argument('--ra', action='store', default=True, dest='random_acc', help='Allow random acceleration')
parser.add_argument('--ofp', action='store', default="output/output.txt", dest='output_file_name',
                    help='Output file path')
parser.add_argument('-i', action='store', default=100, dest='number_of_steps', help='Set a number of steps')
parser.add_argument('-fps', action='store', default=100, dest='fps', help='Set FPS')

results = parser.parse_args()

fps = results.fps
initial_state_file_name = results.initial_state_file_name
output_file_name = results.output_file_name
random_initial_state = results.random_initial_state
random_acc = results.random_acc
number_of_steps = results.number_of_steps
simulator = Simulator(fps)
simulator.fis.log_itself()
for i in range(0, number_of_steps):
    print(i + 1, end=' ')
    simulator = Simulator(fps)
    if not random_initial_state:
        simulator.load_initial_state(initial_state_file_name)
    simulator.start(random_acc)
    simulator.save_state(output_file_name)
