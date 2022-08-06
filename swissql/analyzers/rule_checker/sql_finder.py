from typing import Union
from lark import Tree, Lark
from os import listdir
from os.path import join
from swissql.analyzers.rule_checker.custom_rule import CustomRule
from swissql.analyzers.rule_checker.tree_pattern_find import TreeStringFinder
from swissql.utils.exceptions import Error

class SqlFinder:
    python_parser: Lark
    sql_parser: Lark


    @classmethod
    def __get_parser_from_filename(cls, filename: str) -> Union[Lark]:
        return cls.python_parser

    @classmethod
    def initialize(cls):
        python_grammar_file = 'swissql/analyzers/rule_checker/grammar/python3.lark'
        python_grammar = ''
        with open(python_grammar_file, mode='r') as f:
            python_grammar = f.read()
        cls.python_parser = Lark(
            python_grammar,
            parser='lalr',
            lexer='basic',
            start='file_input',
        )
        sql_grammar_file = 'swissql/analyzers/rule_checker/grammar/sql.lark'
        sql_grammar = ''
        with open(sql_grammar_file, mode='r') as f:
            sql_grammar = f.read()
        cls.sql_parser = Lark(
            sql_grammar,
            parser='lalr',
            lexer='basic',
            start='start',
            propagate_positions=True,
        )

    @classmethod
    def extract_sql_from_file(cls, filename: str) -> list[str]:
        parser = cls.__get_parser_from_filename(filename)
        data = ''
        try:
            with open(filename, mode='r') as f:
                data = f.read()
        except FileNotFoundError as e:
            raise Error('file not found')
        try:
            tree = parser.parse(data)
        except Exception as e:
            raise Error('input file too complicated to parse')
        string_finder = TreeStringFinder()
        string_finder.visit(tree)
        strings = string_finder.strings

        sqls = list()
        for string in strings:
            string = string.strip('"').strip("'")   
            try:
                tree = cls.sql_parser.parse(string)
            except Exception as e:
                continue
            sqls.append(string)
        return sqls
