# import Python's JSON library for its loads() method
import json

# import time for its sleep method
from time import sleep

# import the datetime libraries datetime.now() method
from datetime import datetime

# use the Elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers

# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("localhost:9200")



# define a function that will load a text file
def get_data_from_text_file(self):
# the function will return a list of docs
    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]

# call the function to get the string data containing docs
docs = get_data_from_text_file("name_of_file.json") #add file name here

# print the length of the documents in the string
print ("String docs length:", len(docs))

# define an empty list for the Elasticsearch docs
doc_list = []
history_list=[]

# use Python's enumerate() function to iterate over list of doc strings
for num, doc in enumerate(docs):

# catch any JSON loads() errors
    try:

        # prevent JSONDecodeError resulting from Python uppercase boolean
        doc = doc.replace("True", "true")
        doc = doc.replace("False", "false")

        
        dict_doc = json.loads(doc)
        
        string_dict_doc=str(dict_doc)
        if string_dict_doc not in history_list:
            history_list.append(string_dict_doc)
        else:
            #print("found")
            continue
        

        # append the dict object to the list []
        doc_list += [dict_doc]
        #print("doc_list",doc_list)

    except json.decoder.JSONDecodeError as err:
        # print the errors
        print ("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)

        print ("Dict docs length:", len(doc_list))

    # attempt to index the dictionary entries using the helpers.bulk() method
try:
    print ("\nAttempting to index the list of docs using helpers.bulk()")

    # use the helpers library's Bulk API to index list of Elasticsearch docs
    resp = helpers.bulk(
    client,
    doc_list,
    index = "name_of_your_index",
    doc_type = "_doc"
    )

    # print the response returned by Elasticsearch
    # print ("helpers.bulk() RESPONSE:", resp)
    # print ("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

except Exception as err:

    # print any errors returned w
    ## Prerequisiteshile making the helpers.bulk() API call
    print("Elasticsearch helpers.bulk() ERROR:", err)
    quit()

# get all of docs for the index
# Result window is too large, from + size must be less than or equal to: [10000]
# query_all = {
# 'size' : 10_000,
# 'query': {
# 'match_all' : {}
# }
# }

# print ("\nSleeping for a few seconds to wait for indexing request to finish.")
# sleep(2)

# # pass the query_all dict to search() method
# resp = client.search(
# index = "some_index",
# body = query_all
# )

# print ("search() response:", json.dumps(resp, indent=4))

# # print the number of docs in index
# print ("Length of docs returned by search():", len(resp['hits']['hits']))