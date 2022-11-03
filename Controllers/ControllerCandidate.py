from Models.Candidate import Candidate
from Models.Party import Party
from Repositories.RepositoryCandidate import RepositoryCandidate
from Repositories.RepositoryParty import RepositoryParty


class ControllerCandidate():
    def __init__(self):
        self.repository_candidate = RepositoryCandidate()
        self.repository_party = RepositoryParty()

    def index(self):
        return self.repository_candidate.findAll()

    def create(self,info_candidate):
        new_candidate = Candidate(info_candidate)
        return self.repository_candidate.save(new_candidate)

    def show(self,id):
        the_candidate = Candidate(self.repository_candidate.findById(id))
        return the_candidate.__dict__

    def update(self,id,info_candidate):
        actual_candidate = Candidate(self.repository_candidate.findById(id))
        actual_candidate.cedula = info_candidate["cedula"]
        actual_candidate.num_resolucion = info_candidate["num_resolucion"]
        actual_candidate.nombre = info_candidate["nombre"]
        actual_candidate.apellidos = info_candidate["apellidos"]
        return self.repository_candidate.save(actual_candidate)

    def delete(self,id):
        return self.repository_candidate.delete(id)
    
    # Create relation from one candidate to a party
    def assignParty(self, candidate_id, party_id):
        actual_candidate = Candidate(self.repository_candidate.findById(candidate_id))
        actual_party = Party(self.repository_party.findById(party_id))
        actual_candidate.party = actual_party
        return self.repository_candidate.save(actual_candidate)