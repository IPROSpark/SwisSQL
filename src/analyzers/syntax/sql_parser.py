from lark import Lark, Tree
from src.analyzer.transformers.tree_to_json import TreeToJson

class SqlParser:
    parser: Lark

    @classmethod
    def initialize(cls, lexer='basic'):
        grammar = ''
        with open('grammar/sql.lark', mode='r') as f:
            grammar = f.read()
        parser = Lark(grammar, start='start', lexer=lexer)

    @classmethod
    def parse_spark_sql(cls, sql: str) -> Tree:
        tree = cls.parser.parse(sql)
        return tree
    
    @classmethod
    def parse_spark_sql_as_json(cls, sql: str):
        tree = cls.parse_spark_sql(sql)
        output = TreeToJson().transform(tree)
        return output

    @classmethod
    def parse_spark_sql_as_str(cls, sql: str) -> str:
        tree = cls.parse_spark_sql(sql)
        output = tree.pretty()
        return output
