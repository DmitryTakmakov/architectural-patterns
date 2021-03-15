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
    """
    Abstract parent class for the framework's mappers.
    """

    def __init__(self, conn: Connection):
        """
        Initializes the mapper. Takes in the connection to db,
        creates the cursor for later use and sets up the table name.
        By default it's a blank string, but this name MUST be modified
        in all subclasses.

        :param conn: database connection
        """
        self.connection = conn
        self.cursor = conn.cursor()
        self.table_name = ''

    def return_all(self) -> list:
        """
        Returns all the entries in the given table as a list.
        """
        statement = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def find_by_id(self, entry_id: int) -> tuple:
        """
        Searches the database for an entry with a given ID, returns
        tuple with data. If nothing found, raises an exception.

        :param entry_id: the ID to be searched for
        """
        statement = f'SELECT id, name FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (entry_id,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundError(f'Record with id={entry_id} not found!')

    def insert(self, obj):
        """
        Tries to insert a new entry into the database. If this doesn't
        succeed, raises an exception.

        :param obj: a new object to be inserted
        """
        statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseCommitError(e.args)

    def update(self, obj):
        """
        Tries to update the entry in the database. If it doesn't
        succeed, raises an exception.

        :param obj: object to be updated
        """
        statement = f'UPDATE {self.table_name} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseUpdateError(e.args)

    def delete(self, obj):
        """
        Tries to delete an entry from the database. If that doesn't
        succeed, raises an exception.

        :param obj: object to be deleted
        """
        statement = f'DELETE FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DatabaseDeleteError(e.args)


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
