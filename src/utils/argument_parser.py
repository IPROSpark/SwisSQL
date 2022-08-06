import sys
from argparse import ArgumentParser, Namespace
from src.analyzers.syntax.sql_parser import SqlParser
from src.analyzers.style.sql_formatter import SqlFormatter
from src.utils.schema_reader import SchemaReader
from src.utils.exceptions import Error, exception_handler
from src.analyzers.optimizations.static_optimizer import StaticOptimizer 
from src.manifest import Manifest

class ArgParser:
    parser: ArgumentParser
    args: Namespace

    modes: list[str] = ['syntax', 'format', 'optimize']

    @staticmethod
    def __pair_or(argument: str) -> bool:
        return argument not in sys.argv

    @classmethod
    def __get_query(cls) -> str:
        if cls.args.q:
            return cls.args.q
        elif cls.args.f:
            query = ''
            try:
                with open(cls.args.f, mode='r') as f:
                    query = f.read()
            except FileNotFoundError as e:
                raise Error('query file not found') from e 
            return query
        else:
            raise Error('either -q or -f argument is required')


    @classmethod
    def initialize(cls) -> None:
        optimizers: list[str] = StaticOptimizer.get_optimizers()
        cls.parser = ArgumentParser(
            prog=Manifest.APP_NAME,
            description=Manifest.APP_DESCRIPTION,
        )
        cls.parser.add_argument('mode', choices=cls.modes + ['all',])
        cls.parser.add_argument('-q', required=cls.__pair_or('-f'))
        cls.parser.add_argument('-f', required=cls.__pair_or('-q'))
        cls.parser.add_argument('-s')
        cls.parser.add_argument('-F')
        cls.parser.add_argument('-o', choices=optimizers)
        cls.parser.add_argument('-c')
        cls.parser.add_argument('--output-mode',default='str', choices=['str','json'])

        cls.args = cls.parser.parse_args()

    @classmethod
    @exception_handler()
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
        elif mode == 'optimize':
            schema = None
            
            if cls.args.o in ('optimize', 'qualify_columns'):
                if cls.args.s:
                    schema = SchemaReader.parse_json_schema(cls.args.s)
                elif cls.args.F:
                    schema = SchemaReader.parse_file_json_schema(cls.args.F)
                else:
                    raise Error('schema is not provided')

            print('[Optimizing sql query using sqlglot]')
            print(f'Optimization: {cls.args.o}')
            
            optimized = StaticOptimizer.optimize(cls.args.o, query, schema)
            print(optimized)

        elif mode == 'all':
            for mode in cls.modes:
                cls.choose_analyzer(mode)
                print()
