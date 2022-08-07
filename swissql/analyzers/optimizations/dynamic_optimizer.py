from lark import Lark, Tree
from enum import Enum
from typing import Union, Callable, Optional
from sqlglot import Expression, parse_one
from swissql.analyzers.rule_checker.tree_pattern_find import TreeJoinFinder
from pydantic import BaseModel

class TableSize (BaseModel):
    name : str
    size : float

def dynamic_optimize_join(expr: Tree, table_size: list[TableSize]) -> list[(str, (int, int))]:
    finder = TreeJoinFinder()
    finder.visit(expr)
    spots = finder.join_spots
    hints = []
    
    dic = {}
    for table in table_size:
        dic[table.name] = table.size
    
    for spot in spots:
        name, position = spot
        size = dic[name]
        if size <= 1.5:
            hints.append((f"/*+ BROADCAST({name}) */ ", position))
    return hints


class DynamicOptimizer:

    optimizers = {"dynamic_optimize_joins": dynamic_optimize_join}

    @classmethod
    def optimize(
        cls, optimizer: str, sql: str, table_sizes: list[TableSize]
    ) -> list[(str, (int, int))]:
        sql_grammar_file = "swissql/analyzers/rule_checker/grammar/sql_dynamic.lark"
        sql_grammar = ""
        with open(sql_grammar_file, mode="r") as f:
            sql_grammar = f.read()
        sql_parser = Lark(
            sql_grammar,
            parser="lalr",
            lexer="basic",
            start="start",
            propagate_positions=True,
        )
        expr = sql_parser.parse(sql)
        hints = []
        if optimizer == "optimizer":
            for optimizer in cls.get_optimizers():
                cls.optimize_one(optimizer, expr, table_sizes, hints)
        else:
            cls.optimize_one(optimizer, expr, table_sizes, hints)
        return hints

    @classmethod
    def optimize_one(cls, optimizer: str, expr: Tree, table_sizes: list[TableSize], hints: list):
        optimizer = cls.optimizers[optimizer]
        hint = optimizer(expr, table_sizes)
        if hint:
            hints.extend(hint)

    @classmethod
    def get_optimizers(cls) -> list[str]:
        return list(cls.optimizers.keys())
