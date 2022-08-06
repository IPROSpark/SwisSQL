from typing import Optional
from lark import Lark, Tree
from dataclasses import dataclass

@dataclass
class CustomRule:
    name: str
    grammar: str
    comment: str

    parser: Optional[Lark] = None 

    def __initialise_parser(self) -> None:
        self.parser = Lark(
            self.grammar,
            parser='lalr',
            lexer='basic',
            start='start',
            propagate_positions=True,
        )

    def parse_sql_tree(self, sql: str) -> Tree:
        if not self.parser:
            self.__initialise_parser()
        return self.parser.parse(sql)

    def parse_sql_str(self, sql: str) -> str:
        if not self.parser:
            self.__initialise_parser()
        return repr(self.parser.parse(sql))

