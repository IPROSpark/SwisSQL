from sqlglot import transpile


class SqlFormatter:
    @classmethod
    def format_one(cls, sql: str) -> str:
        statements = transpile(sql,read='spark', write='spark', pretty=True)
        return statements[0]
