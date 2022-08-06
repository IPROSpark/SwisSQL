
import os
import pathlib
from typing import Any, Union
from sqlfluff.cli.commands import cli

class SqlfluffCheck:
    def __init__(self, mode: Union[str,None], file: Union[str,None ] = None, q: Union[str,None] =None, 
                 rules: Union[str,None] =None, dialect: str = None, help: Union[str,None] =None) -> None:
        self.file = file
        self.querry = q
        self.rules = rules
        self.dialect = dialect
        self.mode = mode
        self.help = help
        # TODO пофиксить создание файла
        self.filename = pathlib.Path(__file__).parent.resolve().joinpath(pathlib.Path('intermediate.sql'))
    
    def create_str(self) -> str:
        string = "sqlfluff"
        if self.help:
            return string + ' -' + self.help
        if self.mode:
            string =  string + ' ' + self.mode
        if self.file:
            string =  string + ' ' + self.file
        elif self.querry:
            print(self.filename)
            with open(self.filename, "w") as f:
                f.write(self.querry)
            string = string + ' ' + str(self.filename)
        string = string + ' --dialect ' + self.dialect
        if self.rules:
            string = string + ' --rules' + self.rules
        output = os.popen(string).read()
        if self.querry:
            os.remove(self.filename)
        return output
            
        
