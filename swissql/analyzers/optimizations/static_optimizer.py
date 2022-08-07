from enum import Enum
from typing import Union, Callable, Optional
from sqlglot import Expression, parse_one
from sqlglot.optimizer import optimize
from sqlglot.optimizer.normalize import normalize
from sqlglot.optimizer.eliminate_subqueries import eliminate_subqueries
from sqlglot.optimizer.expand_multi_table_selects import expand_multi_table_selects
from sqlglot.optimizer.isolate_table_selects import isolate_table_selects
from sqlglot.optimizer.optimize_joins import optimize_joins
from sqlglot.optimizer.pushdown_predicates import pushdown_predicates
from sqlglot.optimizer.pushdown_projections import pushdown_projections
from sqlglot.optimizer.qualify_tables import qualify_tables
from sqlglot.optimizer.qualify_columns import qualify_columns
from sqlglot.optimizer.quote_identities import quote_identities
from sqlglot.optimizer.unnest_subqueries import unnest_subqueries


class StaticOptimizer:
    """
    Static optimizer of spark sql query

    ...

    Attributes
    ----------
    optimizers : dict 
        Dict of different optimizers ofr spark sql code

    Methods
    -------
    optimize(cls, optimizer: str, sql: str, schema: Optional[dict] = None)
        Chooses optimizer and using it to generate improved query 
    get_optimizers(cls)
        Return list of available optimizers
    """

    optimizers = {
        "optimize": optimize,
        "normalize": normalize,
        "eliminate_subqueries": eliminate_subqueries,
        "expand_multi_table_selects": expand_multi_table_selects,
        "isolate_table_selects": isolate_table_selects,
        "optimize_joins": optimize_joins,
        "pushdown_predicates": pushdown_predicates,
        "pushdown_projections": pushdown_projections,
        "qualify_tables": qualify_tables,
        "qualify_columns": qualify_columns,
        "quote_identities": quote_identities,
        "unnest_subqueries": unnest_subqueries,
    }

    @classmethod
    def optimize(cls, optimizer: str, sql: str, schema: Optional[dict] = None) -> Expression: 
        """
        Parameters
        ----------
        optimizer: str
            Name of optimizer to be used to optimize spark sql query
        sql: str
            Unoptimized spark sql query
        schema: Optional[dict]
            Dataframe schema to provide additional information before optimization

        Return
        ------
        optimized: Expression
            Optimized spark sql query
        """
        expr = parse_one(sql, read="spark")
        optimizer = cls.optimizers[optimizer]
        # optimized = optimizer(expr,schema).sql(pretty=True)
        if optimizer in ["qualify_columns", "optimize"]:
            optimized = optimizer(expr, schema).sql(pretty=True)
        else:
            optimized = optimizer(expr).sql(pretty=True)
        return optimized

    @classmethod
    def get_optimizers(cls) -> list[str]:
        """
        Parameters
        ----------
        None

        Return
        ------
        keys: list[str]
            List of available optimizers
        """
        return list(cls.optimizers.keys())
