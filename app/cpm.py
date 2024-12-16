from typing import List, Dict, Optional


class Node:
    def __init__(self, activity: int, durations: float, predecessors: List) -> None:
        self.activity = activity
        self.durations = durations
        self.predecessors = predecessors
        self.successors = []
        self.__EarlyStart = None
        self.__EarlyFinish = None
        self.__LateStart = None
        self.__LateFinish = None

    def __str__(self):
        return f"{self.activity}, {self.durations}, {self.predecessors}"


    def set_es(self, es: float) -> None:
        self.__EarlyStart = es


    def set_ef(self, ef: float) -> None:
        self.__EarlyFinish = ef


    def set_ls(self, ls: float) -> None:
        self.__LateStart = ls


    def set_lf(self, lf: float) -> None:
        self.__LateFinish = lf


    def get_es(self) -> float:
        return self.__EarlyStart


    def get_ef(self) -> float:
        return self.__EarlyFinish


    def get_ls(self) -> float:
        return self.__LateStart


    def get_lf(self) -> float:
        return self.__LateFinish


    EarlyStart = property(get_es, set_es)
    EarlyFinish = property(get_ef, set_ef)
    LateStart = property(get_ls, set_ls)
    LateFinish = property(get_lf, set_lf)


class ProjectNetwork:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.end_node_number = None
        self.nodes[0] = Node(0, 0, [])


    def add_node(self, node: Node) -> None:
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of the Node class")
        node_number = node.activity
        if node_number in self.nodes:
            raise ValueError(f"Node with number {node_number} already exists.")

        if (len(node.predecessors) == 0):
            node.predecessors.append(0)

        for predecessor in node.predecessors:
            self.nodes[predecessor].successors.append(node.activity)

        self.nodes[node_number] = node
        self.set_end_node(node_number)


    def set_end_node(self, end_node_number: int) -> None:
        if end_node_number not in self.nodes:
            raise KeyError(f"Node with name {end_node_number} does not exist.")
        self.end_node_number = end_node_number

    def calculate_early_start_and_finish(self) -> None:
        predecessors_for_fin = []
        for node in self.nodes.values():
            if len(node.successors) == 0:
                predecessors_for_fin.append(node.activity)
        if (len(predecessors_for_fin) > 0):
            self.add_node(Node(list(self.nodes.keys())[-1]+1, 0, predecessors_for_fin))

        for node in self.nodes.values():
            if len(node.predecessors) == 0:
                node.set_es(0)
                node.set_ef(node.EarlyStart + node.durations)

        updated = True
        while updated:
            updated = False
            for node in self.nodes.values():
                if node.get_es() is None:
                    max_predecessor_ef = 0
                    for predecessor in node.predecessors:
                        if self.nodes[predecessor].get_ef() is None:
                            break
                        else:
                            max_predecessor_ef = max(max_predecessor_ef, self.nodes[predecessor].get_ef())
                    else:
                        node.set_es(max_predecessor_ef)
                        node.set_ef(node.get_es() + node.durations)
                        updated = True

    def calculate_late_start_and_finish(self) -> None:
        end_node = self.nodes[self.end_node_number]
        end_node.set_lf(end_node.get_ef())
        end_node.set_ls(end_node.get_lf() - end_node.durations)

        # Установим поздние старты и окончания для узлов без преемников
        for node in self.nodes.values():
            if len(self.successors(node)) == 0:
                node.set_lf(node.get_ef())
                node.set_ls(node.get_lf() - node.durations)

        updated = True
        while updated:
            updated = False
            for node in reversed(list(self.nodes.values())):
                if node.get_lf() is None and node != end_node:
                    min_successor_ls = float('inf')
                    for successor in self.successors(node):
                        if successor.get_ls() is None:
                            break
                        else:
                            min_successor_ls = min(min_successor_ls, successor.get_ls())
                    else:
                        node.set_lf(min_successor_ls)
                        node.set_ls(node.get_lf() - node.durations)
                        updated = True
                elif node.get_lf() is None and node == end_node:
                    node.set_lf(node.get_ef())
                    node.set_ls(node.get_lf() - node.durations)
                    updated = True

    def successors(self, node: Node) -> List[Node]:
        successors = []
        for other_node in self.nodes.values():
            if node.activity in other_node.predecessors:
                successors.append(other_node)
        return successors


    def find_critical_path(self) -> List[int]:
        critical_path = []
        for node in self.nodes.values():
            if node.get_es() == node.get_ls() and node.durations > 0:
                critical_path.append(node.activity)
        return critical_path


    def find_all_paths(self, start, path=[]):
        end = list(self.nodes.keys())[-1]
        path = path + [start]
        if start == end:
            yield path
        for node in self.nodes[start].successors:
            if node not in path and (self.nodes[node].get_lf() - self.nodes[node].get_ef() == 0):
                yield from self.find_all_paths(node, path)


    def find_critical_paths(self, start):
        all_paths = list(self.find_all_paths(start))
        max_time = 0
        critical_paths = []
        for path in all_paths:
            path_time = sum(self.nodes[task].durations for task in path)
            if path_time > max_time:
                max_time = path_time
                critical_paths = [path]
            elif path_time == max_time:
                critical_paths.append(path)

        return critical_paths, max_time


    def get_cp_duration(self, cp: List[int]) -> float:
        duration = 0
        for i in cp:
            duration += self.nodes[i].durations
        return duration

    def print(self) -> None:
        for node in self.nodes.values():
            print(
                f"№{node.activity}, ES = {node.EarlyStart}, EF = {node.EarlyFinish}, LS = {node.LateStart}, LF={node.LateFinish}")
