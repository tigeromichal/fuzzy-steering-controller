import matplotlib.pyplot as plt
from Defuzzifier import Defuzzifier
from Fuzzifier import Fuzzifier
from InferenceEngine import InferenceEngine


class FuzzyInferenceSystem:
    def __init__(self):
        self.fuzzifier = Fuzzifier()
        self.inference_engine = InferenceEngine()
        self.defuzzifier = Defuzzifier()

    def generate_response(self, model):
        car_A = model.cars["A"]
        car_B = model.cars["B"]
        car_C = model.cars["C"]
        d_BA = car_B.get_distance_from(car_A)
        d_CA = car_C.get_distance_from(car_A)
        crisp_input_data = InputData(car_A.vx, car_B.vx, car_C.vx, d_BA, d_CA, model.road_length - car_A.x, car_A.lane)
        fuzzy_input_data = self.fuzzifier.fuzzify(crisp_input_data)
        fuzzy_part_conclusion = self.inference_engine.generate_fuzzy_conclusion(fuzzy_input_data)
        crisp_part_conclusion = self.inference_engine.generate_crisp_conclusion(crisp_input_data)
        crisp_conclusion = self.defuzzifier.defuzzify(fuzzy_part_conclusion)
        ax = min(crisp_conclusion, crisp_part_conclusion['ax'])
        lane = crisp_part_conclusion['lane']
        return OutputData(ax, lane)

    def log_itself(self):
        i = 1
        sets = self.fuzzifier.fuzzy_sets
        for key in sets:
            if key == "d_endA":
                break;
            handles = []
            plt.figure(i)
            plt.title(key)
            for subkey in sets[key].subsets:
                points_x = [point['x'] for point in sets[key].subsets[subkey].points]
                points_y = [point['y'] for point in sets[key].subsets[subkey].points]
                handle, = plt.plot(points_x, points_y, label=subkey)
                plt.ylabel("μ(x)")
                plt.xlabel("x")
                handles.append(handle)
            plt.legend(handles=handles)
            plt.show()
        sets = self.inference_engine.fuzzy_sets
        for key in sets:
            handles = []
            plt.figure(i)
            plt.title(key)
            for subkey in sets[key].subsets:
                points_x = [point['x'] for point in sets[key].subsets[subkey].points]
                points_y = [point['y'] for point in sets[key].subsets[subkey].points]
                handle, = plt.plot(points_x, points_y, label=subkey)
                plt.ylabel("μ(x)")
                plt.xlabel("x")
                handles.append(handle)
            plt.legend(handles=handles)
            plt.show()


class InputData:
    def __init__(self, v_A, v_B, v_C, d_BA, d_CA, d_endA, lane_A):
        self.values = {
            "v_A": v_A, "v_B": v_B, "v_C": v_C, "d_BA": d_BA, "d_CA": d_CA, "d_endA": d_endA, "lane_A": lane_A}


class OutputData:
    def __init__(self, ax, lane):
        self.values = {"ax": ax, "lane": lane}
