from lark import Tree, Visitor

class TreePatternFinder(Visitor):
    positions: list[(int, int)] = []

    def pattern(self, tree):
        self.positions.append((tree.meta.line, tree.meta.column))


class TreeStringFinder(Visitor):
    strings: list[str] = []
    
    def string(self, tree):
        for el in tree.children:
            self.strings.append(el.value)


