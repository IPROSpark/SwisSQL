from lark import Tree, Visitor

class TreePatternFinder(Visitor):
    positions: list[(int, int)] = []

    def pattern(self, tree):
        self.positions.append((tree.meta.line, tree.meta.column))

class TreeSqlFinder(Visitor):
    start_positions: list[(int, int)] = []
    end_positions: list[(int, int)] = []

    def sql_string(self, tree):
        self.start_positions.append((tree.meta.line, tree.meta.column))

