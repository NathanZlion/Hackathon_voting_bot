from typing import Optional, Any

import pymongo
from datetime import datetime

import config


class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(config.mongodb_connection_string)
        self.db = self.client["Hackathon2024VotingCount"]

        self.user_collection = self.db["user"]
        self.vote_collection = self.db["vote"]

    ####################################################################
    # User functions
    ####################################################################

    def check_if_user_exists(self, user_id: int, raise_exception: bool = False):
        if self.user_collection.count_documents({"_id": user_id}) > 0:
            return True
        else:
            if raise_exception:
                raise ValueError(f"User {user_id} does not exist")
            else:
                return False

    def add_new_user(
        self,
        user_id: int,
        username: str = "",
        first_name: str = "",
        last_name: str = "",
    ):
        user_dict = {
            "_id": user_id,

            "username": username,
            "first_name": first_name,
            "last_name": last_name,

            "last_interaction": datetime.now(),
            "first_seen": datetime.now(),
        }

        if not self.check_if_user_exists(user_id):
            self.user_collection.insert_one(user_dict)


    def set_user_attribute(self, user_id: int, key: str, value: Any):
        self.check_if_user_exists(user_id, raise_exception=True)
        self.user_collection.update_one({"_id": user_id}, {"$set": {key: value}})
    


    ####################################################################
    # Vote functions
    ####################################################################

    def add_new_vote(self, user_id: int, project_id: int):
        # since one user can only vote for one project, we can use the user_id as the unique identifier

        vote_dict = {
            "user_id": user_id,
            "project_id": project_id,
            "timestamp": datetime.now(),
        }

        self.vote_collection.insert_one(vote_dict)

    
    def get_vote_by_user_id(self, user_id: int):
        return self.vote_collection.find_one({"user_id": user_id})

    
    def get_votes_by_project_id(self, project_id: int):
        return self.vote_collection.count_documents({"project_id": project_id})

    
    def get_total_votes(self):
        return self.vote_collection.count_documents({})


    def retract_vote(self, user_id: int):
        self.vote_collection.delete_many({"user_id": user_id})

