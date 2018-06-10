class Defuzzifier:
    @staticmethod
    def defuzzify(fuzzy_set):
        return Defuzzifier.defuzzify_separate_subsets_centres_weigthed_sum(fuzzy_set)

    @staticmethod
    def defuzzify_separate_subsets_centres_weigthed_sum(fuzzy_set):
        sum_y = 0
        sum_xy = 0
        for key in fuzzy_set.subsets:
            n = len(fuzzy_set.subsets[key].points)
            center_x = (fuzzy_set.subsets[key].points[0]['x'] + fuzzy_set.subsets[key].points[n - 1]['x']) / 2
            p1 = 0
            p2 = 0
            for i in range(1, n):
                if fuzzy_set.subsets[key].points[i]['x'] >= center_x:
                    p1 = fuzzy_set.subsets[key].points[i - 1]
                    p2 = fuzzy_set.subsets[key].points[i]
                    break
            y = 0
            if p1['x'] != p2['x']:
                a = (p2['y'] - p1['y']) / (p2['x'] - p1['x'])
                b = p1['y'] - a * p1['x']
                y = a * center_x + b
            sum_y += y
            sum_xy += center_x * y
        if sum_y == 0:
            return 0
        else:
            return sum_xy / sum_y
