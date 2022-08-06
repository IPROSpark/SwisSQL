from lark import Tree, Visitor

class TreePatternFind(Visitor):
    positions: list[(int, int)] = []

    def pattern(self, tree):
        self.positions.append((tree.meta.line, tree.meta.column))

