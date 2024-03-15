'''
data_parser.py - intakes the Raw Amazon data and parses it down to the required
usable parts for the rest of the project

Not usable for the turned in version since we do not have the review data in the
GitHub repository since the file sizes are too large. 


'''
import json
import csv
import os

def parse_json_file(filepath, file_name):
    '''
    Parses an Amazon review data "json" file
    param:
    filepath - path to amazon review data files
    file_name - name of the file. Used for the categories. 
    yields - csv formatted review data
    '''
    assert(isinstance(filepath, str) and isinstance(file_name, str))
    with open(filepath, 'r', encoding='UTF8') as f:
        items = f.read().split('\n')
        for item in items:
            if len(item) > 0:
                item = json.loads(item)
                outputList = [file_name, #"Source Category"
                            getKey(item,'asin'), #"Product ID"
                            getKey(item,'reviewerID'), #"Reviewer ID"
                            getKey(item,'overall'), #"Rating"
                            getKey(item,'summary'), #"Review Summary"
                            getKey(item,'reviewText'), #"Review Text"
                            getKey(item,'verified')]
                outputList.append("image" in item.keys()) #"Has Image"
                yield outputList

def load_metadata(filepath):
    '''
    Pulls the metadata information
    params: 
    filepath - filepath to metadata
    '''
    assert(isinstance(filepath, str))
    with open(filepath, 'r', encoding="UTF8") as f:
        items = f.read().split('\n')
        returnDict = {}
        for item in items:
            if len(item) > 0:
                item = json.loads(item)
                returnDict[getKey(item,"asin")] = getKey(item,"price")
        return returnDict

def find_metadata(metadict, asin):
    '''
    Simple helper function to find a product id in the metadata
    params: 
    metadict - Metadata dict
    asin - the product ID to search for
    '''
    assert(isinstance(metadict, dict))
    assert(isinstance(asin, str))
    return getKey(metadict, asin)

def getKey(mydict,key):
    '''
    Does a search for a key with a try catch to just keep it cleaner
    params:
    dict - input dict
    key - input key
    '''
    assert(isinstance(mydict, dict))
    try:
        return mydict[key]
    except KeyError:
        return "N/A"

def process_reviews_folder(folder_path, meta_path):
    '''
    processes the entire folder of review data
    param:
    folder_path - the path to the folder with the review data
    meta_path - path to the metadata folder

    ### DO NOT PUT THE METADATA FOLDERS INSIDE THE REVIEW DATA FOLDER!! METADATA SHOULD BE IN ITS OWN PATH
    '''
    assert(isinstance(folder_path, str) and isinstance(meta_path, str))
    with open("filtered_reviews.csv", "a", encoding="UTF8") as w:
        writer = csv.writer(w, lineterminator="\n")
        writer.writerow(["Source Category", "Product ID","Reviewer ID", "Rating", "Review Summary","Review Text", "Has Image", "Verified", "Product Price"])
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return

        # Iterate through each file in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if the item is a file and ends with .json
            if os.path.isfile(file_path) and filename.endswith('.json'):
                print(f"Processing file: {filename}")
                # Process the JSON file
                category = filename.split("_5")[0]+".json"
                metapath = meta_path+"/meta_"+category
                metadict = load_metadata(metapath)
                for outputList in parse_json_file(file_path, filename):
                    price = find_metadata(metadict, outputList[1])
                    outputList.append(price)
                    writer.writerow(outputList)

process_reviews_folder("./reviews")
