from json import loads
from json.decoder import JSONDecodeError
from swissql.utils.exceptions import Error

class SchemaReader:

    @staticmethod
    def parse_json_schema(json_schema: str) -> dict:
        try:
            schema = loads(json_schema)
        except JSONDecodeError as e:
            raise Error('Schema is not in json format')
        
        return schema

    @classmethod
    def parse_file_json_schema(cls, filename: str) -> dict:
        json_schema = ''
        try:
            with open(filename, mode='r') as f:
                json_schema = f.read()
        except FileNotFoundError as e:
            raise Error('Schema file is not found')
        schema = cls.parse_json_schema(json_schema)
        return schema
