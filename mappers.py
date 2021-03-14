from models import *
from orm.mappers import Mapper, MapperRegistry


class StudentMapper(Mapper):
    def __init__(self, connection):
        super().__init__(connection)
        self.table_name = 'students'


class ProjectMapperRegistry(MapperRegistry):
    mappers = {
        'student': StudentMapper
    }
    models = {Student}

    def __init__(self, connection):
        super().__init__(connection)
