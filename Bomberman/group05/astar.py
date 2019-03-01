class Node:

    def __init__(self, x, y, parent = None):
        self.point = [x, y]
        self.x = x
        self.y = y
        self.parent = parent

        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

    def calculate_md(self, end):

        return abs(self.point.x - self.end.x) + abs(self.point.y - self.end.y)

    def is_same(self, compare_node):

        if (abs(compare_node.point.x - self.point.x) and abs(compare_node.point.y - self.point.y)):
            return True
        else:
            return False

class Astar:

    def __init__(self, start, end, wrld):

        self.width = wrld.width
        self.height = wrld.height
        self.start_node = Node(start[0], start[1])
        self.end_node = Node(end[0], start[0])

    def find_path(self, wrld):
        evaluated = []

        notEvaluated = [[self.start_node.f_cost, self.start_node]]

        notEvalCheck = []
        notEvalCheck.append(self.start_node)

        previous_steps = {}

        g_cost = {}
        f_cost = {}

        g_cost[self.start_node] = 0

        path_found = False

        while not len(notEvalCheck) < 1 and not path_found:

            notEvaluated.sort(reverse=False, key=lambda x: x[0])
            current_node = notEvaluated[0][1]
            notEvalCheck.remove(current_node)

            if current_node.is_same(self.end_node):

                path_found = True

                return previous_steps

            evaluated.append(current_node)

            x = current_node.point.x
            y = current_node.point.y

            for i in range(3):

                i -= 1

                for j in range(3):

                    j -= 1

                    # if the postition is in world bounds
                    if not (x + i >= self.width or x + i < 0 or y + j >= self.height or y + j < 0):

                        neighbor = Node(x + i, y + j)

                        if neighbor in evaluated:

                            continue

                        tentative_gcost = g_cost[current_node] + self.find_gcost(neighbor, )

                        if not notEvalCheck.__contains__(neighbor):

                            g_cost[neighbor] = tentative_gcost
                            f_cost[neighbor] = g_cost[neighbor] + self.find_heuristiccost(neighbor, wrld)

                            notEvaluated.put((f_cost[neighbor], neighbor))
                            notEvalCheck.append(neighbor)

                        elif (tentative_gcost >= g_cost[neighbor]):

                            continue

                    previous_steps[neighbor] = current_node

                    g_cost[neighbor] = tentative_gcost
                    f_cost[neighbor] = abs(g_cost[neighbor]) + abs(self.find_heuristiccost(neighbor, wrld))

        if not path_found:

            print("\n ----------NO PATH REACHED ---------")

    def find_gcost(self, node, wrld):
        return 1

    def find_heuristiccost(self, node, wrld):
        return self.manhattan_distance(node, self.end_node)

    def manhattan_distance(self,node_1, node_2):

        return abs(node_1.x - node_2.x) + abs(node_1.y - node_2.y)