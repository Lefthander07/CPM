from typing import List, Dict, Optional

class Node:
    def __init__(self, activity: int, durations: float, predecessors: tuple) -> None:
        self.activity = activity
        self.durations = durations
        self.predecessors = predecessors
        self.__EarlyStart = None
        self.__EarlyFinish = None
        self.__LateStart =  None
        self.__LateFinish = None

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

    def add_node(self, node: Node) -> None:
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of the Node class")
        node_number = node.activity
        if node_number in self.nodes:
            raise ValueError(f"Node with number {node_number} already exists.")

        self.nodes[node_number] = node
        self.set_end_node(node_number)

    def set_end_node(self, end_node_number: int) -> None:
        if end_node_number not in self.nodes:
            raise KeyError(f"Node with name {end_node_number} does not exist.")
        self.end_node_number = end_node_number

    def calculate_early_start_and_finish(self) -> None:
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

    def find_critical_path(self) -> List[Node]:
        critical_path = []
        current_node = self.nodes[self.end_node_number]
        while current_node is not None:
            critical_path.insert(0, current_node.activity)
            if len(current_node.predecessors) > 0:
                for predecessor in current_node.predecessors:
                    if self.nodes[predecessor].get_ef() == current_node.get_ls():
                        current_node = self.nodes[predecessor]
                        break
            else:
                current_node = None
        return critical_path

    def get_cp_duration(self, cp: List[int]) -> float:
        duration = 0
        for i in cp:
            duration += self.nodes[i].durations
        return duration

    def print(self) -> None:
        for node in self.nodes.values():
            print(f"№{node.activity}, ES = {node.EarlyStart}, EF = {node.EarlyFinish}, LS = {node.LateStart}, LF={node.LateFinish}")

if __name__ == "__main__":
    A = Node(1, 5, {})
    B = Node(2, 6, {1})
    C = Node(3, 3, {1})
    D = Node(4, 4, {2})
    E = Node(5, 2, {2, 3})
    F = Node(6, 1, {4, 5})

    project = ProjectNetwork()

    project.add_node(A)
    project.add_node(B)
    project.add_node(C)
    project.add_node(D)
    project.add_node(E)
    project.add_node(F)

    project.calculate_early_start_and_finish()
    project.calculate_late_start_and_finish()
    cp = project.find_critical_path()
    duration_cp = project.get_cp_duration(cp)
    print(cp)
    print(duration_cp)