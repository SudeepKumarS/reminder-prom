import pymongo

from common.settings import CONNECTION_STRING

client = pymongo.MongoClient(CONNECTION_STRING)


def get_collection_from_db(db_name: str, collection_name: str):
    """
    Helper function to retreive a collection from a database
    """
    db = client.get_database(db_name)
    return db.get_collection(collection_name)
