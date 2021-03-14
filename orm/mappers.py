"""
Module containing abstract mappers for the framework's ORM as well as the
registry parent class for existing mappers. Actual mappers to be used
in the project have to be subclassed to the Mapper class from here
as well as the MapperRegistry implementations.
"""
from sqlite3 import Connection

from orm.errors import RecordNotFoundError, DatabaseCommitError, \
    DatabaseUpdateError, DatabaseDeleteError


class Mapper:
    def __init__(self, conn: Connection):
        self.connection = conn
        self.cursor = conn.cursor()
        self.table_name = ''

    def return_all(self) -> list:
        statement = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def find_by_id(self, id: int):
        statement = f'SELECT id, name FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundError(f'Record with id={id} not found!')

    def insert(self, obj):
        statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseCommitError(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.table_name} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseUpdateError(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseDeleteError(e.args)


# TODO separate mappers for all types of objects in the framework

class MapperRegistry:
    """
    Mappers registry parent class. It stores all available data mappers
    in the class-attribute dictionary. It can return the mapper on
    demand.
    """
    mappers = dict()
    models = set()

    def __init__(self, connection: Connection):
        """
        Initializes the registry with the database connection.

        :param connection: connection to database (sqlite3 by default)
        """
        self.connection = connection

    def get_mapper(self, obj: Mapper):
        """
        Returns a relevant mapper. The method checks the instance of
        the object passed into it and returns the relevant mapper.

        :param obj: instance of one of models
        :return: relevant data mapper object
        """
        for key, value in self.mappers.items():
            for model in self.models:
                if isinstance(obj, model):
                    return value(self.connection)

    def get_current_mapper(self, name: str):
        """
        Returns a relevant mapper by name. Checks if the string
        passed into it corresponds to a name in the class-attribute
        dictionary. Returns the relevant data mapper if it does.

        :param name: the data mapper name
        :return: relevant data mapper object
        """
        return self.mappers[name](self.connection)
