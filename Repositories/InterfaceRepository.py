import pymongo
import certifi
from bson import DBRef
from bson.objectid import ObjectId
from typing import TypeVar, Generic, List, get_origin, get_args
import json


T = TypeVar('T')

class InterfaceRepository(Generic[T]):
    def __init__ (self):
        ca = certifi.where()

        dataConfig = self.loadFileConfig()
        client = pymongo.MongoClient(dataConfig["data-db-connection"],
                                     tlsCAFile=ca)
        self.database_name = client[dataConfig["name-db"]]
        the_class = get_args(self.__orig_bases__[0])
        self.collection = the_class[0].__name__.lower()

    def loadFileConfig (self):
        with open('config.json') as f:
            data = json.load(f)
        return data

    def save (self,item: T):
        the_collection = self.database_name[self.collection]
        the_id = ""
        item = self.transformRefs(item)
        if hasattr(item,"_id") and item._id!="":
            the_id = item._id
            _id = ObjectId(the_id)
            the_collection = self.database_name[self.collection]
            delattr(item,"_id")
            item = item.__dict__
            update_item = {"$set": item}
            element = the_collection.update_one({"_id": _id},update_item)
        else:
            _id = the_collection.insert_one(item.__dict__)
            the_id = _id.inserted_id.__str__()
        element = the_collection.find_one({"_id": ObjectId(the_id)})
        element["_id"] = element["_id"].__str__()
        return self.findById(the_id)

    def delete(self, id):
        the_collection = self.database_name[self.collection]
        count = the_collection.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": count}

    def update (self,id,item: T):
        _id = ObjectId(id)
        the_collection = self.database_name[self.collection]
        delattr(item,"_id")
        item = item.__dict__
        update_item = {"$set": item}
        count = the_collection.update_one({"_id": _id},update_item)
        return {"updated_count": count.matched_count}

    def findById (self,id):
        the_collection = self.database_name[self.collection]

        element = the_collection.find_one({"_id": ObjectId(id)})
        element = self.getValuesDBRef(element)
        if element==None:
            element = {}
        else:
            element["_id"] = element["_id"].__str__()
        return element

    def findAll (self):
        the_collection = self.database_name[self.collection]
        data = []
        for element in the_collection.find():
            element["_id"] = element["_id"].__str__()
            element = self.transformObjectIds(element)
            element = self.getValuesDBRef(element)
            data.append(element)
        return data

    def query (self,the_query):
        the_collection = self.database_name[self.collection]
        data = []
        for element in the_collection.find(the_query):
            element["_id"] = element["_id"].__str__()
            element = self.transformObjectIds(element)
            element = self.getValuesDBRef(element)
            data.append(element)
        return data

    def queryAggregation (self,the_query):
        the_collection = self.database_name[self.collection]
        data = []
        for element in the_collection.aggregate(the_query):
            element["_id"] = element["_id"].__str__()
            element = self.transformObjectIds(element)
            element = self.getValuesDBRef(element)
            data.append(element)
        return data

    def getValuesDBRef (self,element):
        keys = element.keys()
        for key in keys:
            if isinstance(element[key],DBRef):
                the_collection = self.database_name[element[key].collection]
                valor = the_collection.find_one({"_id": ObjectId(element[key].id)})
                valor["_id"] = valor["_id"].__str__()
                element[key] = valor
                element[key] = self.getValuesDBRef(element[key])
            elif isinstance(element[key],list) and len(element[key]) > 0:
                element[key] = self.getValuesDBRefFromList(element[key])
            elif isinstance(element[key],dict):
                element[key] = self.getValuesDBRef(element[key])
        return element

    def getValuesDBRefFromList(self, theList):
        new_list = []
        the_collection = self.database_name[theList[0]._id.collection]
        for item in theList:
            value = the_collection.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            new_list.append(value)
        return new_list

    def transformObjectIds(self, element):
        for attribute in element.keys():
            if isinstance(element[attribute], ObjectId):
                element[attribute] = element[attribute].__str__()
            elif isinstance(element[attribute], list):
                element[attribute] = self.formatList(element[attribute])
            elif  isinstance(element[attribute], dict):
                element[attribute]=self.transformObjectIds(element[attribute])
        return element

    def formatList(self, element):
        new_list = []
        for item in element:
            if isinstance(item, ObjectId):
                new_list.append(item.__str__())
        if len(new_list) == 0:
            new_list = element
        return new_list

    def transformRefs(self, item):
        the_dict = item.__dict__
        keys = list(the_dict.keys())
        for key in keys:
            if the_dict[key].__str__().count("object") == 1:
                newObject = self.ObjectToDBRef(getattr(item, key))
                setattr(item, key, newObject)
        return item

    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))