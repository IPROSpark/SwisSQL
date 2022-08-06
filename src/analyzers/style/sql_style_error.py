
from typing import Any
from sqlfluff.cli.commands import cli

def sqlfluff_check(*args: Any, **kwargs: Any) -> str:
    cli()
