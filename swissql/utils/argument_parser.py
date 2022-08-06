import sys
import os
from argparse import ArgumentParser, Namespace
from swissql.analyzers.style.sql_style_error import SqlfluffCheck
from swissql.analyzers.anti_pattern.anti_pattern_finder import AntiPatternFinder
from swissql.analyzers.syntax.sql_parser import SqlParser
from swissql.analyzers.style.sql_formatter import SqlFormatter
from swissql.utils.schema_reader import SchemaReader
from swissql.utils.exceptions import Error, exception_handler
from swissql.analyzers.optimizations.static_optimizer import StaticOptimizer
from swissql.analyzers.rule_checker.rule_finder import RuleFinder
from swissql.analyzers.rule_checker.custom_rule import CustomRule
from swissql.analyzers.rule_checker.sql_finder import SqlFinder
from swissql.manifest import Manifest


class ArgParser:
    parser: ArgumentParser
    args: Namespace
    modes: list[str] = ["syntax", "format", "optimize", "style", "anti_pattern", "extract", "rule"]

    @staticmethod
    def __pair_or(argument: str) -> bool:
        return argument not in sys.argv

    @staticmethod
    def __pair_and(argument: str) -> bool:
        return argument in sys.argv

    @classmethod
    def __get_query(cls) -> str:
        if cls.args.q:
            return cls.args.q
        elif cls.args.f:
            query = ""
            try:
                with open(cls.args.f, mode="r") as f:
                    query = f.read()
            except FileNotFoundError as e:
                raise Error("query file not found") from e
            return query
        else:
            raise Error("either -q or -f argument is required")

    @classmethod
    def initialize(cls) -> None:
        RuleFinder.initialize()
        
        rules = RuleFinder.get_rules()       
        optimizers: list[str] = StaticOptimizer.get_optimizers()
        cls.parser = ArgumentParser(
            prog=Manifest.APP_NAME,
            description=Manifest.APP_DESCRIPTION,
        )
        cls.parser.add_argument(
            "mode", choices=cls.modes + ["all", "style"], help="mode of operation"
        )
        cls.parser.add_argument(
            "-q",
            # "--query",
            required=cls.__pair_or("-f"),
            help="specify SQL query",
        )
        cls.parser.add_argument(
            "-f",
            # "--file-sql",
            required=cls.__pair_or("-q"),
            help="specify file to read SQL query from",
        )
        cls.parser.add_argument(
            "-s",
            # "--schema",
            help="""specify schema:
        Schema is a mapping in one of
            the following forms:\n
                1. {table: {col: type}}\n
                2. {db: {table: {col: type}}}\n
                3. {catalog: {db: {table: {col: type}}}}\n
        Example types: INT, STRING""",
        )
        cls.parser.add_argument(
            "-F",
            # "--File-schema",
            help="specify schema file to read schema from",
        )
        cls.parser.add_argument(
            "-o",
            #  "--optimizer",
            choices=optimizers,
            help="specify optimizers",
        )
        cls.parser.add_argument(
            '-r',
            # "--rule",
            choices=rules+['all',],
            help='specify rule file'
        )
        # cls.parser.add_argument("-c", help="specify")
        cls.parser.add_argument(
            "--dialect", default="sparksql", help="specify sqlfluff dialect"
        )
        cls.parser.add_argument(
            "--output-mode",
            default="str",
            choices=["str", "json"],
            help="specify output format",
        )
        cls.args = cls.parser.parse_args()

    @classmethod
    @exception_handler()
    def choose_analyzer(cls, mode=None) -> None:
        mode = cls.args.mode if mode is None else mode
        if mode == 'extract':
            SqlFinder.initialize()
            if not cls.args.f:
                raise Error('no file provided')
            filename = cls.args.f
            print('\u001b[33m[Extracting Spark SQLs from file using lark]\u001b[0m')
            sqls = SqlFinder.extract_sql_from_file(filename)
            if sqls:
                print('Found:')
                for sql in sqls:
                    print(sql)
            else:
                print('Did not find any SQLs')
            return
        
        
        query = cls.__get_query()
        if mode == "syntax":
            print("\u001b[33m[Generating syntax tree using sqlglot]\u001b[0m")
            output = SqlParser.parse_tree(query)
            print(output)
        elif mode == "format":
            print("\u001b[33m[Formatting sql query using sqlglot]\u001b[0m")
            output = SqlFormatter.format_one(query)
            print(output)
        elif mode == "style":
            print("\u001b[33m[Style sql query use sqlfluff]\u001b[0m")
            # получаем ссылку на файл с помощью lark
            # print(cls.args.f)
            output = SqlfluffCheck(
                "lint",
                file=cls.args.f,
                q=cls.args.q,
                rules=cls.args.rules,
                dialect=cls.args.dialect,
            ).create_str()
            print(output)
            #
            # Меняем позиции в тексте
        elif mode == "optimize":
            schema = None
            if cls.args.o in ("optimize", "qualify_columns"):
                if cls.args.s:
                    schema = SchemaReader.parse_json_schema(cls.args.s)
                elif cls.args.F:
                    schema = SchemaReader.parse_file_json_schema(cls.args.F)
                else:
                    raise Error("schema is not provided")

            print("\u001b[33m[Optimizing sql query using sqlglot]\u001b[0m")
            print(f"Optimization: {cls.args.o}")
            optimized = StaticOptimizer.optimize(cls.args.o, query, schema)
            print(optimized)

        elif mode == "anti_pattern":
            print("\u001b[33m[Detecting anti-patterns using sqlcheck]\u001b[0m")

            # TODO: add verbosity level option
            instance = AntiPatternFinder(verbose=True)
            sqlcheck_output = ""
            if cls.args.f:
                sqlcheck_output = instance.find_anti_patterns_from_file(cls.args.f)
            elif cls.args.q:
                sqlcheck_output = instance.find_anti_patterns_from_query(cls.args.q)
            else:
                raise Error("either -q or -f argument is required")
            print(sqlcheck_output)
        elif mode == 'rule':
            rule = cls.args.r
            if not rule:
                raise Error('no rule specified')
            if rule == 'all':
                RuleFinder.load_rules()
            else:
                RuleFinder.load_rule(rule)
            found = RuleFinder.find_rules(query)
            print('\u001b[33m[Finding rules using lark]\u001b[0m')
            for rule in found:
                print(f'Rule {rule[0].name} found:')
                print(f'Position: {rule[1][0]}, {rule[1][1]}')
                print(f'Comment: {rule[0].comment}')
                print()
                
        elif mode == "all":
            for mode in cls.modes:
                cls.choose_analyzer(mode)
                print()
