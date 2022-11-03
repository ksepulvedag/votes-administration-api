from Models.Party import Party
from Repositories.RepositoryParty import RepositoryParty


class ControllerParty():
    def __init__(self):
        self.repository_party = RepositoryParty()

    def index(self):
        return self.repository_party.findAll()

    def create(self,info_party):
        new_party = Party(info_party)
        return self.repository_party.save(new_party)

    def show(self,id):
        the_party = Party(self.repository_party.findById(id))
        return the_party.__dict__

    def update(self,id,info_party):
        actual_party = Party(self.repository_party.findById(id))
        actual_party.nombre = info_party["nombre"]
        actual_party.lema = info_party["lema"]
        return self.repository_party.save(actual_party)

    def delete(self,id):
        return self.repository_party.delete(id)