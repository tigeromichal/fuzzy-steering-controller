import copy
from xml.dom import minidom

from FuzzySet import FuzzySet
from FuzzySet import FuzzySubSet
from RuleBase import RuleBase


class InferenceEngine:
    def __init__(self):
        self.rule_base = RuleBase()
        self.fuzzy_sets = dict()
        self.file_name = "data/outputFuzzySets-triangular-risky.xml"
        self.load_from_xml(self.file_name)
        # self.log_itself()

    def generate_fuzzy_conclusion(self, input):
        conjunctions = dict()
        for rule in self.rule_base.rules:
            conjunction = 1000
            for antecedent in rule.antecendents:
                #                              input["v_A"]["slow"] // = for example 0.7
                conjunction = min(conjunction, input[antecedent[0]][antecedent[1]])
                # print (antecedent, rule.consequent, input[antecedent[0]][antecedent[1]])
            if rule.consequent in conjunctions:
                conjunctions[rule.consequent] = max(conjunctions[rule.consequent], conjunction)
            else:
                conjunctions[rule.consequent] = conjunction
        subsets = dict()
        for consequent in conjunctions:
            subsets[consequent] = copy.deepcopy(self.fuzzy_sets["acceleration"].subsets[consequent]).cut_to(
                conjunctions[consequent])
        return FuzzySet(subsets)

    def generate_crisp_conclusion(self, input):
        # calculate max acceleration that doesn't exceed vx = 25 m/s after 1 second
        ax = 25 - input.values['v_A']
        lane = 0
        # if overtaking and car B behind, come back to right lane
        if input.values['lane_A'] == 0 and input.values['d_BA'] < -2:
            lane = 1
        # if overtaking and car C too close and car B far enough, come back to right lane
        elif input.values['lane_A'] == 0 and (input.values['d_CA'] > 0 and input.values['d_CA'] <= 27) and (
                        input.values['d_BA'] > 2 or input.values['d_BA'] < -2):
            lane = 1
        # if car A goes fast enough and car B is close and car C and the end of the road are far enough, begin overtaking
        elif input.values['lane_A'] == 1 and input.values['v_A'] > 20 and input.values['v_B'] < 25 and (
                        input.values['d_BA'] > 0 and input.values['d_BA'] < 27) and (
                        input.values['d_CA'] > 52 or input.values['d_CA'] < -2) and input.values['d_endA'] > 100:
            lane = 0
        # else stay on the lane
        else:
            lane = input.values['lane_A']
        return {'ax': ax, 'lane': lane}

    def load_from_xml(self, file_name):
        DOM_tree = minidom.parse(file_name)
        sets_root = DOM_tree.childNodes.item(0)
        set_nodes = sets_root.getElementsByTagName("set")
        for set_node in set_nodes:
            what = set_node.getAttributeNode("what").childNodes[0].toxml()
            subset_nodes = set_node.getElementsByTagName("subset")
            subsets = dict()
            for subset_node in subset_nodes:
                value = subset_node.getAttributeNode("value").childNodes[0].toxml()
                point_nodes = subset_node.getElementsByTagName("point")
                points = [{'x': float(point_node.getAttributeNode("x").childNodes[0].toxml()),
                           'y': float(point_node.getAttributeNode("y").childNodes[0].toxml())} for point_node in
                          point_nodes]
                subsets[value] = FuzzySubSet(points, value)
            self.fuzzy_sets[what] = FuzzySet(subsets)

    def log_itself(self):
        print("Output fuzzy sets loaded from file \"" + self.file_name + "\":")
        for key in self.fuzzy_sets:
            print(key, ':')
            self.fuzzy_sets[key].log_itself()
