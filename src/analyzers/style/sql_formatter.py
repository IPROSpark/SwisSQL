from sqlglot import transpile

class SqlFormatter:

    @classmethod
    def format_one(cls, sql: str) -> str:
        statements = transpile(sql,read='postgres', write='spark', pretty=True)
        return statements[0]


