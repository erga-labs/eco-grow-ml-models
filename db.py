from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from secret import AppwriteSecrets


def get_record():
    s = AppwriteSecrets()
    client = Client()

    client.set_endpoint(s.ENDPOINT) 

    client.set_project(s.PROJECT_ID)               
    
    client.set_key(s.API_KEY)                       
    client.set_self_signed(True)
    db = Databases(client)
    db_ID = s.DB_ID 
    collection_ID = s.COLLECTION_ID
    result = db.list_documents(db_ID, collection_ID)
    return result['documents'][0]
    


if __name__ == '__main__':
    print(get_record())