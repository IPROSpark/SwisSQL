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


class TreeJoinFinder(Visitor):
    join_spots: list[(str, (int, int))] = []

    def from_item_pattern(self, tree):
        try:
            name = tree.children[0].children[0].children[0].value
            meta = tree.children[0].children[0].meta
            position = (meta.line, meta.column)
            self.join_spots.append((name, position))
        except Exception:
            return
