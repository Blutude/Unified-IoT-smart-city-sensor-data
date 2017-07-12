from Azure import *

# have another method/query for timeouts. (not needed right now)
def readAzureBlocks(id):
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()

    query = {'query': 'SELECT VALUE Block FROM c JOIN Block IN c.Blocks WHERE c.deviceID = \"' + id + '\"'}

    options = {}
    options['enableCrossPartitionQuery'] = True

    docs = client.QueryDocuments(coll_link, query, options)
    #docs = client.ReadDocuments(coll_link)

    return list(docs)

def writeAzure(dict):
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()
    client.CreateDocument(coll_link, dict)