from Repositories.InterfaceRepository import InterfaceRepository
from Models.Result import Result

from bson.objectid import ObjectId


class RepositoryResult(InterfaceRepository[Result]):
    
    def get_list_votes_per_table(self, table_id):
        query = {"mesa.$id": ObjectId(table_id)}

        return self.query(query)
    
    def get_most_voted_per_table(self):
        query = {
                    "$group": {
                        "_id": "$mesa",
                        "max": {
                            "$max": "$cant_votos"
                        },
                        "doc": {
                            "$first": "$$ROOT"
                        }
                    }
                }
        
        pipeline = [query]
        return self.queryAggregation(pipeline)
    
    def get_average_votes_per_table(self, table_id):
        query1 =    {
                        "$match": {"mesa.$id": ObjectId(table_id)}
                    }
                    
        query2 =    {
                        "$group": {
                            "_id": "$mesa",
                            "promedio": {
                                "$avg": "$cant_votos"
                            }
                            }
                    }
        pipeline = [query1,query2]
        return self.queryAggregation(pipeline)