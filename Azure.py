import pydocumentdb.document_client as document_client
from Constants import Constants

def getCosmosDBClient():
    # Initialize the Python DocumentDB client
    client = document_client.DocumentClient(Constants.URL, {'masterKey': Constants.KEY})
    return client

def getCosmosDBColl_link():
    client = getCosmosDBClient()

    success = False
    while not success:
        try:
            db_id = Constants.DATABASE_NAME
            db_query = "select * from r where r.id = '{0}'".format(db_id)
            db = list(client.QueryDatabases(db_query))[0]
            db_link = db['_self']

            coll_id = Constants.COLL_NAME
            coll_query = "select * from r where r.id = '{0}'".format(coll_id)
            coll = list(client.QueryCollections(db_link, coll_query))
            if coll:
                coll = coll[0]
            else:
                raise ValueError("Collection not found in database.")
            coll_link = coll['_self']
            success = True
        except Exception as e:
            print(str(e))
    print("Successfully connected to database")

    return coll_link