from xml.dom import minidom
from FuzzySet import FuzzySet
from FuzzySet import FuzzySubSet


class Fuzzifier:
    def __init__(self):
        self.fuzzy_sets = dict()
        self.file_name = "data/inputFuzzySets-triangular-risky.xml"
        self.load_from_xml(self.file_name)
        # self.log_itself()

    def fuzzify(self, input_data):
        out = dict()
        for key in input_data.values:
            out[key] = self.fuzzy_sets[key].membership_function(input_data.values[key])
        return out

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
        print("Input fuzzy sets loaded from file \"" + self.file_name + "\":")
        for key in self.fuzzy_sets:
            print(key, ':')
            self.fuzzy_sets[key].log_itself()