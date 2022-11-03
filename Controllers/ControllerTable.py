from Models.Table import Table
from Repositories.RepositoryTable import RepositoryTable


class ControllerTable():
    def __init__(self):
        self.repository_table = RepositoryTable()

    def index(self):
        return self.repository_table.findAll()

    def create(self,info_table):
        new_table = Table(info_table)
        return self.repository_table.save(new_table)

    def show(self,id):
        the_table = Table(self.repository_table.findById(id))
        return the_table.__dict__

    def update(self,id,info_table):
        actual_table = Table(self.repository_table.findById(id))
        actual_table.num_mesa = info_table["num_mesa"]
        actual_table.cant_inscritos = info_table["cant_inscritos"]
        return self.repository_table.save(actual_table)

    def delete(self,id):
        return self.repository_table.delete(id)