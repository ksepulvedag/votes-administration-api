from Models.Result import Result
from Models.Candidate import Candidate
from Models.Table import Table
from Repositories.RepositoryResult import RepositoryResult
from Repositories.RepositoryCandidate import RepositoryCandidate
from Repositories.RepositoryTable import RepositoryTable


class ControllerResult():
    def __init__(self):
        self.repository_result = RepositoryResult()
        self.repository_candidate = RepositoryCandidate()
        self.repository_table = RepositoryTable()

    def index(self):
        return self.repository_result.findAll()

    # Create and relate a new result with a candidate and a table
    def create(self,result_info, candidate_id, table_id):
        new_result_info = Result(result_info)
        candidate_info = Candidate(self.repository_candidate.findById(candidate_id))
        table_info = Table(self.repository_table.findById(table_id))

        new_result_info.candidato = candidate_info
        new_result_info.mesa = table_info

        return self.repository_result.save(new_result_info)

    def show(self,id):
        the_result = Result(self.repository_result.findById(id))
        return the_result.__dict__

    def update(self,result_id, candidate_id, result_info, table_id):
        new_result_info = Result(self.repository_result.findById(result_id))
        candidate_info = Candidate(self.repository_candidate.findById(candidate_id))
        table_info = Table(self.repository_table.findById(table_id))
        new_result_info.cant_votos = result_info["cant_votos"]

        new_result_info.candidato = candidate_info
        new_result_info.mesa = table_info

        return self.repository_result.save(new_result_info)

    def delete(self,id):
        return self.repository_result.delete(id)
    
    
    def list_votes_per_table(self, table_id):
        return self.repository_result.get_list_votes_per_table(table_id)
    
    def most_voted_per_table(self):
        return self.repository_result.get_most_voted_per_table()
    
    def average_votes_per_table(self, table_id):
        return self.repository_result.get_average_votes_per_table(table_id)