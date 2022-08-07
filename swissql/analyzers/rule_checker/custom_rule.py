from typing import Optional
from lark import Lark, Tree
from dataclasses import dataclass


@dataclass
class CustomRule:
    """
    Dataclass for user defined rules

    ...

    Attributes
    ----------
    name: str
        Filename of rule file
    grammar: str
        Grammar as pattern for finding user defined rules in query
    comment: str
        User defined comment to acknowledge a problem and/or to give insights to how to fix it
    parser: Optional[Lark]
        Rule parser that is used to find user defined patterns

    Methods
    -------
    __initialise_parser()
        Creates parser based on grammar
    parse_sql_tree(sql: str)
        Parses sql query and returns it's tree
    parse_sql_str(sql: str)
        Parses sql query and returns it's tree as string representation
    """

    name: str
    grammar: str
    comment: str

    parser: Optional[Lark] = None

    def __initialise_parser(self) -> None:
        """
        Parameters
        ----------
        None

        Return
        ------
        None
        """
        self.parser = Lark(
            self.grammar,
<<<<<<< HEAD
            parser="lalr",
            lexer="basic",
            start="start",
            propagate_positions=True,
=======
            parser='lalr',
            lexer='basic',
            start='start',
            propagate_positions=True, # allows to store node position
>>>>>>> refs/remotes/origin/main
        )

    def parse_sql_tree(self, sql: str) -> Tree:
        """
        Attributes
        ----------
        sql: str
            Spark sql query to be parsed

        Return
        ------
        tree: Tree
            Parsed sql query tree
        """
        if not self.parser:
            self.__initialise_parser()
        return self.parser.parse(sql)

    def parse_sql_str(self, sql: str) -> str:
        """
        Attributes
        ----------
        sql: str
            Spark sql query to be parsed

        Return
        ------
        tree: str
            String representation of parsed tree
        """
        if not self.parser:
            self.__initialise_parser()
        return repr(self.parser.parse(sql))
