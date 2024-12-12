import typing
import


class Node:
    def __init__(self, activity: float, durations: float, predecessors: tuple) -> None:
        self.activity = activity
        self.durations = durations
        self.predecessors = predecessors
        self.__EarlyStart = None
        self.__EarlyFinish = None
        self.__LateStart =  None
        self.__LateFinish = None

    def setES(self, ES: float) -> None:
        self.__EarlyStart = ES
        self.EarlyFinish = self.EarlyStart + self.durations
    def setEF(self, EF: float) -> None:
        self.__EarlyFinish = EF
    def setLS(self, LS: float) -> None:
        self.__LateStart = LS
    def setLF(self, LF: float) -> None:
        self.__EarlyStart = LF

    def getES(self) -> float:
        return self.__EarlyStart
    def getEF(self) -> float:
        return self.__EarlyFinish
    def getLS(self) -> float:
        return self.__LateStart
    def getLF(self) -> float:
        return self.__EarlyStart

    EarlyStart = property(getES, setES)
    EarlyFinish = property(getEF, setEF)
    LateStart = property(getLS, setLS)
    LateFinish = property(getLF, setLF)


if __name__ == "__main__":
    A = Node(1,2, (3,1))
    print(A.EarlyStart)

class ProjectNetwork:
    def __init__(self, ):
        pass
    def calculate_early_start_and_finish(self) -> None:
        pass
    def calculate_late_start_and_finish(self) -> None:
        pass
    def add_node(self, node: Node) -> None:
        pass
    def find_critical_path(self) -> Node:
        pass


