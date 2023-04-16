import heapq
import matplotlib.pyplot as plt


class Node:
    def __init__(self, name):
        self.name = name
        self.adjacent = {}
        self.distance = float('inf')
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, weight):
        self.adjacent[neighbor] = weight

    def __lt__(self, other):
        return self.distance < other.distance


class Dijkstra:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.name] = node

    def get_node(self, name):
        return self.nodes.get(name)

    def get_shortest_path(self, start_node_name, end_node_name):
        start_node = self.get_node(start_node_name)
        end_node = self.get_node(end_node_name)

        start_node.distance = 0
        unvisited_nodes = [(0, start_node)]

        while unvisited_nodes:
            heapq.heapify(unvisited_nodes)
            current_node = heapq.heappop(unvisited_nodes)[1]

            if current_node == end_node:
                path = []
                while current_node.previous:
                    path.append(current_node.name)
                    current_node = current_node.previous
                path.append(start_node.name)
                return path[::-1]

            current_node.visited = True
            for neighbor, weight in current_node.adjacent.items():
                if not neighbor.visited:
                    new_distance = current_node.distance + weight
                    if new_distance < neighbor.distance:
                        neighbor.distance = new_distance
                        neighbor.previous = current_node
                        heapq.heappush(unvisited_nodes, (new_distance, neighbor))

    def plot_graph(self):
        for node in self.nodes.values():
            for neighbor, weight in node.adjacent.items():
                plt.plot([node.name, neighbor.name], [node.distance, neighbor.distance], 'bo-')
        plt.xlabel('Nodes')
        plt.ylabel('Distance')
        plt.show()


if __name__ == '__main__':
    # 使用 Dijkstra 算法计算最短路径
    graph = Dijkstra()

    # 添加节点
    graph.add_node(Node('A'))
    graph.add_node(Node('B'))
    graph.add_node(Node('C'))
    graph.add_node(Node('D'))
    graph.add_node(Node('E'))
    graph.add_node(Node('F'))

    # 添加边
    graph.get_node('A').add_neighbor(graph.get_node('B'), 7)
    graph.get_node('A').add_neighbor(graph.get_node('C'), 9)
    graph.get_node('A').add_neighbor(graph.get_node('F'), 14)
    graph.get_node('B').add_neighbor(graph.get_node('C'), 10)
    graph.get_node('B').add_neighbor(graph.get_node('D'), 15)
    graph.get_node('C').add_neighbor(graph.get_node('D'), 11)
    graph.get_node('C').add_neighbor(graph.get_node('F'), 2)
    graph.get_node('D').add_neighbor(graph.get_node('E'), 6)
    graph.get_node('E').add_neighbor(graph.get_node('F'), 9)

    shortest_path = graph.get_shortest_path('A', 'E')
    print(shortest_path)

    graph.plot_graph()
