# Example for extracting SQL from a file:

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType
from datetime import datetime, date
from pyspark.sql import Row

def init_spark():
    spark = SparkSession.builder.appName("HelloWorld").getOrCreate()
    sc = spark.sparkContext
    return spark, sc


# SQl Queries
sql_queries = [
    'SELECT * FROM table1;',
    'SELECT * FROM table1 WHERE id = 1;',
    'SELECT * FROM table1 WHERE id = 1 AND name = "John" OR name = "Jane" OR name = "Jack";',
]

def main():
    spark_sql_queries = [
        "SELECT * FROM table",
    ]


    spark, sc = init_spark()
    df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
    ])
    df.createOrReplaceGlobalTempView("tableA")
    spark.sql("select * from tableA").show()


if __name__ == "__main__":
    main()

