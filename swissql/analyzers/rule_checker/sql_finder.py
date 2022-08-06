import re
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
    def __get_parser_from_filename(cls, filename: str) -> Lark:
        return cls.python_parser

    @classmethod
    def initialize(cls):
        # python_grammar_file = 'swissql/analyzers/rule_checker/grammar/python_peg.lark'
        # python_grammar = ''
        # with open(python_grammar_file, mode='r') as f:
        #     python_grammar = f.read()
        # cls.python_parser = Lark(
        #     python_grammar,
        #     parser='lalr',
        #     lexer='basic',
        #     start='start',
        # )
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
        data = ''
        try:
            with open(filename, mode='r') as f:
                data = f.read()
        except FileNotFoundError as e:
            raise Error('file not found')

        # Extract strings from data
        strings = re.findall(r"('''|\"\"\"|[\"'])((?:\\.|.)*?)\1", data)
        sqls = list()
        for string in strings:
            string = ''.join(string)
            string = string.strip('"').strip("'").strip(';')   
            try:
                tree = cls.sql_parser.parse(string)
            except Exception as e:
                continue
            sqls.append(string)
        return sqls
