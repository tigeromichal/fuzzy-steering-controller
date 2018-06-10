from xml.dom import minidom


class RuleBase:
    def __init__(self):
        self.rules = list()
        self.file_name = "data/ruleBase.xml"
        self.load_from_xml(self.file_name)
        # self.log_itself()

    def load_from_xml(self, file_name):
        DOM_tree = minidom.parse(file_name)
        rules_root = DOM_tree.childNodes.item(0)
        rule_nodes = rules_root.getElementsByTagName("rule")
        for rule_node in rule_nodes:
            antecendent_nodes = rule_node.getElementsByTagName("antecedent")
            antecendents = [(antecendent_node.getAttributeNode("what").childNodes[0].toxml(),
                             antecendent_node.childNodes[0].toxml()) for antecendent_node in antecendent_nodes]
            consequent_node = rule_node.getElementsByTagName("consequent")
            consequent = consequent_node[0].childNodes[0].toxml()
            self.rules.append(Rule(antecendents, consequent))

    def log_itself(self):
        print("Rules loaded from file \"" + self.file_name + "\":")
        for rule in self.rules:
            print('IF ', end='')
            n = len(rule.antecendents)
            for i in range(0, n):
                print(rule.antecendents[i][0] + " IS " + rule.antecendents[i][1], end='')
                if n > 1 and i < n - 1:
                    print(" AND ", end='')
            print(" THEN", rule.consequent)


class Rule:
    def __init__(self, antecendents, consequent):
        self.antecendents = antecendents
        self.consequent = consequent
