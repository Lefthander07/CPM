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
        self.EarlyFinish = self.EarlyStart + self.durations
    def set_ef(self, ef: float) -> None:
        self.__EarlyFinish = ef
    def set_ls(self, ls: float) -> None:
        self.__LateStart = ls
    def set_lf(self, lf: float) -> None:
        self.__EarlyStart = lf

    def get_es(self) -> float:
        return self.__EarlyStart
    def get_ef(self) -> float:
        return self.__EarlyFinish
    def get_ls(self) -> float:
        return self.__LateStart
    def get_lf(self) -> float:
        return self.__EarlyStart

    EarlyStart = property(get_es, set_es)
    EarlyFinish = property(get_ef, set_ef)
    LateStart = property(get_ls, set_ls)
    LateFinish = property(get_lf, set_lf)


if __name__ == "__main__":
    A = Node(1,2, (3,1))
    print(A.EarlyStart)

class ProjectNetwork:
    def __init__(self, ):
        self.nodes: Dict[int, Node] = {}
        self.end_node_number = None

    def add_node(self, node: Node) -> None:
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of the Node class")
        node_number = node.activity
        if node_number in self.nodes:
            raise ValueError(f"Node with number {node_number} already exists.")

        self.nodes[node_number] = node

    def calculate_early_start_and_finish(self) -> None:
        pass
    def calculate_late_start_and_finish(self) -> None:
        pass
    def find_critical_path(self) -> Node:
        pass


