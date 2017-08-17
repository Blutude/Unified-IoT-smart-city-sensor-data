from Azure import *

def readDayAzureRadars(id, date):
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()

    query = {'query': 'SELECT VALUE Block FROM c JOIN Block IN c.Blocks WHERE c.deviceID = \"' + id + '\" AND Block.StartDateTime >= \"' + date + '\" AND Block.StartDateTime < \"' + date + " 99:99:99" + '\"'}

    options = {}
    options['enableCrossPartitionQuery'] = True

    docs = client.QueryDocuments(coll_link, query, options)
    #docs = client.ReadDocuments(coll_link)

    return list(docs)

def writeAzure(dict):
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()
    client.CreateDocument(coll_link, dict)

def replaceAzureDict(dict, doc_link):
    client = getCosmosDBClient()
    client.ReplaceDocument(doc_link, dict)

def readAzureTempDict():
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()

    query = {'query': 'SELECT * FROM c WHERE c.deviceID = \"old-tp01p01\"'}

    # options = {}
    # options['enableCrossPartitionQuery'] = True

    docs = client.QueryDocuments(coll_link, query)  # , options)
    # docs = client.ReadDocuments(coll_link)

    doc = list(docs)[0]
    doc_link = doc['_self']

    return (doc, doc_link)

def readAzureLevelDict():
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()

    query = {'query': 'SELECT * FROM c WHERE c.deviceID = \"old-lvl01p02\"'}

    # options = {}
    # options['enableCrossPartitionQuery'] = True

    docs = client.QueryDocuments(coll_link, query)  # , options)
    # docs = client.ReadDocuments(coll_link)

    doc = list(docs)[0]
    doc_link = doc['_self']

    return (doc, doc_link)

def readAzureGPSDict():
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()

    query = {'query': 'SELECT * FROM c WHERE c.deviceID = \"old-gps01p35\"'}

    # options = {}
    # options['enableCrossPartitionQuery'] = True

    docs = client.QueryDocuments(coll_link, query)  # , options)
    # docs = client.ReadDocuments(coll_link)

    doc = list(docs)[0]
    doc_link = doc['_self']

    return (doc, doc_link)

def readDayAzureTempDict(date):
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()

    query = {
        'query': 'SELECT VALUE Block FROM c JOIN Block IN c.Blocks WHERE c.deviceID = \"old-tp01p01\" AND Block.datetime >= \"' + date + '\" AND Block.datetime < \"' + date + "T99:99:99" + '\"'}

    # options = {}
    # options['enableCrossPartitionQuery'] = True

    docs = client.QueryDocuments(coll_link, query)  # , options)
    # docs = client.ReadDocuments(coll_link)

    return (list(docs))

def readDayAzureLevelDict(date):
    client = getCosmosDBClient()
    coll_link = getCosmosDBColl_link()

    query = {
        'query': 'SELECT VALUE Block FROM c JOIN Block IN c.Blocks WHERE c.deviceID = \"old-lvl01p02\" AND Block.datetime >= \"' + date + '\" AND Block.datetime < \"' + date + "T99:99:99" + '\"'}

    # options = {}
    # options['enableCrossPartitionQuery'] = True

    docs = client.QueryDocuments(coll_link, query)  # , options)
    # docs = client.ReadDocuments(coll_link)

    return (list(docs))