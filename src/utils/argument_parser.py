import sys
from argparse import ArgumentParser, Namespace
from src.analyzers.syntax.sql_parser import SqlParser
from src.analyzers.style.sql_formatter import SqlFormatter

class ArgParser:
    parser: ArgumentParser
    args: Namespace

    modes: list[str] = ['syntax', 'format']

    @staticmethod
    def __pair_or(argument: str) -> bool:
        return argument not in sys.argv

    @classmethod
    def __get_query(cls) -> str:
        if cls.args.q:
            return cls.args.q
        elif cls.args.f:
            query = ''
            with open(cls.args.f, mode='r') as f:
                query = f.read()
            return query
        else:
            cls.parser.error('either -q or -f argument is required')


    @classmethod
    def initialize(cls) -> None:
        cls.parser = ArgumentParser(
            prog='Swissql',
            description='Spark SQL analytic engine',
        )
        cls.parser.add_argument('mode', choices=cls.modes + ['all',])
        cls.parser.add_argument('-q', required=cls.__pair_or('-f'))
        cls.parser.add_argument('-f', required=cls.__pair_or('-q'))
        cls.parser.add_argument('--output-mode',default='str', choices=['str','json'])

        cls.args = cls.parser.parse_args()

    @classmethod
    def choose_analyzer(cls, mode=None) -> None:
        mode = cls.args.mode if mode is None else mode
        query = cls.__get_query()
        if mode == 'syntax':
            print('[Generating syntax tree using sqlglot]')
            output = SqlParser.parse_tree(query)
            print(output)
        elif mode == 'format':
            print('[Formatting sql query using sqlglot]')
            output = SqlFormatter.format_one(query)
            print(output)
        elif mode == 'all':
            for mode in cls.modes:
                cls.choose_analyzer(mode)
                print()
