from typing import Union
from lark import Tree, Lark
from os import listdir
from os.path import join
from src.analyzers.rule_checker.custom_rule import CustomRule
from src.analyzers.rule_checker.tree_pattern_find import TreeSqlFinder
from src.utils.exceptions import Error

class SqlFinder:
    python_parser: Lark


    @classmethod
    def __get_parser_from_filename(cls, filename: str) -> Union[Lark]:
        return cls.python_parser

    @classmethod
    def initialize(cls):
        sql_grammar_file = 'src/analyzers/rule_checker/grammar/python3.lark'
        grammar = ''
        with open(sql_grammar_file, mode='r') as f:
            grammar = f.read()
        cls.python_parser = Lark(
            grammar,
            parser='lalr',
            lexer='basic',
            start='file_input',
            propagate_positions=True,
        )

    @classmethod
    def extract_sql_from_file(cls, filename: str) -> list[(int, int)]:
        parser = cls.__get_parser_from_filename(filename)
        data = ''
        with open(filename, mode='r') as f:
            data = f.read()
        tree = parser.parse(data)
        print(tree)
        finder = TreeSqlFinder()
        finder.visit(tree)
        start_positions = finder.start_positions
        return start_positions
