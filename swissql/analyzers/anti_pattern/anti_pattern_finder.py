import os

from swissql.utils.exceptions import Error


class AntiPatternFinder:
    def __init__(self, verbose: bool = True):
        """
        Initialize the AntiPatternFinder class
        AntiPatternFinder is a class that can be used to find anti-patterns in sql statements
        It uses the sqlcheck command to find anti-patterns

        :param verbose: if True, verbose flag will be passed to sqlcheck

        """
        self.verbose: bool = verbose
        self.temp_sql_file: str = "temp.sql"

        # Check sqlcheck availability in system
        self.isavailable = os.system("sqlcheck -version") == 0
        if not self.isavailable:
            raise Error("sqlcheck not found in system")

    def find_anti_patterns_from_file(self, sql_filename: str) -> str:
        """
        Find anti-patterns in sql statement from file

        :param sql_filename: sql file name
        :return: sqlcheck output
        """
        # Check availability of sqlcheck
        if not self.isavailable:
            raise Error("sqlcheck not found in system")

        # Run sqlcheck on sqlfile
        # Timeout in case of wrong sqlfile
        # TODO: switch timeout 1 to subprocess timeout to improve crossplatform compatibility
        sqlcheck_output = os.popen(
            f"timeout 1 sqlcheck -c {'-v' if self.verbose else ''} -f { sql_filename }"
        ).read()
        return sqlcheck_output

    def find_anti_patterns_from_query(self, sql: str) -> str:
        """
        Find anti-patterns in sql statement

        :param sql: sql statement
        :return: sqlcheck output
        """
        # Check availability of sqlcheck
        if not self.isavailable:
            raise Exception("sqlcheck not found in system")

        # Using writing to file to provide crossplatform compatibility
        with open(self.temp_sql_file, "w") as f:
            f.write(sql)
        sqlcheck_output = self.find_anti_patterns_from_file(self.temp_sql_file)
        os.remove(self.temp_sql_file)

        return sqlcheck_output

    @staticmethod
    def sqlcheck_output_to_json(sqlcheck_output: str) -> str:
        """?"""
        pass


if __name__ == "__main__":
    # Use example
    instance = AntiPatternFinder(verbose=True)
    print(instance.find_anti_patterns_from_query("select * from table"))
    print(instance.find_anti_patterns_from_file("../../../examples/example2.sql"))
