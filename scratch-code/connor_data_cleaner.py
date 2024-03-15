import json
import csv
import os

def parse_json_file(filepath, file_name):
    with open(filepath, 'r', encoding='UTF8') as f:
        items = f.read().split('\n')
        returnDict = {"Reviews": []}
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
    with open(filepath, 'r', encoding="UTF8") as f:
        items = f.read().split('\n')
        returnDict = {}
        for item in items:
            if len(item) > 0:
                item = json.loads(item)
                returnDict[getKey(item,"asin")] = getKey(item,"price")
        return returnDict

def find_metadata(metadict, asin):
    return getKey(metadict, asin)

def getKey(dict,key):
    try:
        return dict[key]
    except KeyError:
        return "N/A"

def process_reviews_folder(folder_path):
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
                metapath = "metadata/meta_"+category
                metadict = load_metadata(metapath)
                for outputList in parse_json_file(file_path, filename):
                    price = find_metadata(metadict, outputList[1])
                    outputList.append(price)
                    writer.writerow(outputList)

process_reviews_folder("./reviews")
