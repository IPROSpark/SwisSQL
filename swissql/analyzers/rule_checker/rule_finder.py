from lark import Tree
from os import listdir
from os.path import join
from swissql.analyzers.rule_checker.custom_rule import CustomRule
from swissql.analyzers.rule_checker.tree_pattern_find import TreePatternFinder
from swissql.utils.exceptions import Error

class RuleFinder:
    SPLITTER: str = ':END_OF_COMMENT:'
    PATTERN: str = 'PATTERN'
    
    rules_dir: str = 'rules'
    rules: list[CustomRule] = []
    rule_files: list[str] = []



    @classmethod
    def __get_rule_names(cls) -> list[str]:
        files = listdir(cls.rules_dir)
        files = list(filter(lambda x: x != '__init__.py', files))
        return files

    @classmethod
    def __parse_rule_file(cls, data: str) -> tuple[str]:
        try:
            comment, grammar = data.split(cls.SPLITTER)
            return (comment, grammar)
        except ValueError as e:
            raise Error('invalid rule file format') from e


    @classmethod
    def initialize(cls):
        cls.rule_files = cls.__get_rule_names()
        

    @classmethod
    def load_rule(cls, rule_file: str):
        data = ''
        with open(join(cls.rules_dir,rule_file), mode='r') as f:
            data = f.read()
        comment, grammar = cls.__parse_rule_file(data)
        cls.rules.append(CustomRule(
            name=rule_file,
            grammar=grammar,
            comment=comment
        ))

    @classmethod
    def load_rules(cls):
        for rule_file in cls.rule_files:
            cls.load_rule(rule_file)            
    
    @classmethod
    def get_rules(cls) -> list[str]:
        return list(cls.rule_files)

    @classmethod
    def find_rules(cls, sql: str) -> list[(CustomRule, list[(int, int)])]:
        found = list()
        for rule in cls.rules:
            try:
                tree = rule.parse_sql_tree(sql)
            except Exception as e:
                continue
            finder = TreePatternFinder()
            finder.visit(tree)
            if len(finder.positions) > 0:
                found.append((rule, finder.positions))
        return found

