from argparse import ArgumentParser
from src.analyzers.syntax.sql_parser import SqlParser

class ArgParser:
    parser: ArgumentParser
    args: 

    @classmethod
    def initialize(cls) -> None:
        cls.parser = ArgumentParser(
            prog='Swissql',
            description='Spark SQL analytic engine',
        )
        cls.parser.add_argument('sql')
        cls.parser.add_argument('--mode', required=True, choices=['syntax',])
        cls.parser.add_argument('--output-mode',default='str', choices=['str','json'])
        cls.args = cls.parser.parse_args()
    
    @classmethod
    def choose_analyzer(cls) -> None:
        match cls.args.mode:
            case 'syntax':
                SqlParser.initialize()
                output = SqlParser.parse_spark_sql(sql)
                print(output)
