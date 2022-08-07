from typing import List


class Manifest:
    APP_NAME: str = "swissql"
    APP_DESCRIPTION: str = "Spark SQL analytic engine"
    APP_VERSION: str = "v0.2.5.2"
    LICENSE: str = "GNU"
    EMAIL: str = "andrey24072002@bk.ru"
    REQUIREMENTS: List = [
        "lark>=1.1.2",
        "sqlfluff>=1.2.1",
        "sqlglot>=4.2.9",
        "pydantic>=1.9.1",
    ]
    AUTHORS_GIT: str = "husker Nicialy Quakumei"
    GIT_URL: str = "https://github.com/IPROSpark/SparkSQL-Analyzer"
