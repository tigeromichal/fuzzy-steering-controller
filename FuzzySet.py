class FuzzySet:
    def __init__(self, subsets):
        self.subsets = subsets

    def membership_function(self, x):
        out = dict()
        for key in self.subsets:
            out[key] = self.subsets[key].membership_function(x)
        return out

    def log_itself(self):
        for key in self.subsets:
            self.subsets[key].log_itself()
            print()


class FuzzySubSet:
    def __init__(self, points, value):
        self.points = points
        self.value = value

    def membership_function(self, x):
        n = len(self.points)
        if x <= self.points[0]['x']:
            return self.points[0]['y']
        if x >= self.points[n - 1]['x']:
            return self.points[n - 1]['y']
        p1 = 0
        p2 = 0
        for i in range(1, n):
            if self.points[i]['x'] >= x:
                p1 = self.points[i - 1]
                p2 = self.points[i]
                break
        parameters = find_linear_equation_parameters(p1, p2)
        return parameters['a'] * x + parameters['b']

    def cut_to(self, y):
        n = len(self.points)
        i = 0
        while i < n:
            if self.points[i]['y'] > y:
                first_point_index = i
                points_above_count = 1
                j = i + 1
                while self.points[j]['y'] > y and j < n:
                    points_above_count += 1
                    j += 1
                last_point_index = first_point_index + points_above_count - 1
                # polyline starting from above
                if first_point_index == 0:
                    # only one point (singleton) or all points above
                    if last_point_index == n - 1:
                        self.points[last_point_index]['y'] = y
                    # some of the points not above - need to find linear equation
                    else:
                        # move the point
                        parameters = find_linear_equation_parameters(self.points[last_point_index],
                                                                     self.points[last_point_index + 1])
                        self.points[last_point_index] = {'x': (y - parameters['b']) / parameters['a'], 'y': y}
                        # remove previous points (if any exist) to simplify polyline
                        j = first_point_index
                        while j < last_point_index:
                            self.points.remove(self.points[j])
                            j += 1
                # polyline starting from below
                else:
                    # only one point above - have to double the point
                    if points_above_count == 1:
                        # left point
                        parameters = find_linear_equation_parameters(self.points[last_point_index],
                                                                     self.points[last_point_index - 1])
                        p1 = {'x': (y - parameters['b']) / parameters['a'], 'y': y}
                        # right point
                        parameters = find_linear_equation_parameters(self.points[last_point_index],
                                                                     self.points[last_point_index + 1])
                        p2 = {'x': (y - parameters['b']) / parameters['a'], 'y': y}
                        # replace the single point with left point
                        self.points[first_point_index] = p1
                        # insert new right point to the list
                        self.points.insert(last_point_index + 1, p2)
                    # two points above or more - move edge points and remove all the points between them
                    elif points_above_count >= 2:
                        # left point
                        parameters = find_linear_equation_parameters(self.points[first_point_index],
                                                                     self.points[first_point_index - 1])
                        p1 = {'x': (y - parameters['b']) / parameters['a'], 'y': y}
                        # right point
                        parameters = find_linear_equation_parameters(self.points[last_point_index],
                                                                     self.points[last_point_index + 1])
                        p2 = {'x': (y - parameters['b']) / parameters['a'], 'y': y}
                        self.points[first_point_index] = p1
                        self.points[last_point_index] = p2
                        j = first_point_index + 1
                        while j < last_point_index - 1:
                            self.points.remove(self.points[j])
                            j += 1
            i += 1
        return self

    def log_itself(self):
        print(self.value, end=' ')
        n = len(self.points)
        for i in range(0, n):
            print('(' + str(self.points[i]['x']) + ', ' + str(self.points[i]['y']), end=')')
            if n > 1 and i < n - 1:
                print(', ', end='')


def find_linear_equation_parameters(p1, p2):
    a = (p2['y'] - p1['y']) / (p2['x'] - p1['x'])
    b = p1['y'] - a * p1['x']
    return {'a': a, 'b': b}
