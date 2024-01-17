
# Here is the MS documentation for this libary: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme?view=azure-python
# And even more detailed here: https://learn.microsoft.com/en-us/python/api/azure-ai-textanalytics/azure.ai.textanalytics?view=azure-python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import json

# Initialize some useful variables. 
psalms_filename = "OT-21_Psalms.json"
proverbs_filename = "OT-22_Proverbs.json"
matthew_filename = "NT-01_Matthew.json"
mark_filename = "NT-02_Mark.json"
luke_filename = "NT-03_Luke.json"
john_filename = "NT-04_John.json"
isiah_filename = "OT-27_Isaiah.json"


# This function reads the bible book and returns a dictionary of chapters.
# If flat = 1, then it is flattened such that each chatper is a single string. 
# If flat = 2, then the entire book is flattened into a single string.
# If flat is neithher 1 nor 2, then the book is returned as a dictiaonry of dicationaries.
def scripture_book_reader(filename, flat = None):

    datapath = "datasets\CPDV-JSON\\" # This is the path to the JSON files.

    try:
        # Opening JSON file containing Psalms
        f = open(datapath + filename, encoding='utf-8')
        
        # returns JSON object as 
        # a dictionary
        filedata = json.load(f)
        
        # Closing file
        f.close()
    except Exception as e:
        print(f"Error! Could not open the file called {filename} in {datapath}. Is there such a file? Error statement: {e}")
        return None

    # If it is returned as a dictionary of dictionaries, then we are done.
    if flat != 1 :
        if flat != 2:
            return filedata
              
    ag_list = []
    ag_dict = dict()

    # Read over every chapter. 
    for chapter in list(filedata.keys())[:-1]:
        
        # Start with the empty string that will be built up and added to each list element. 
        inter_text = ""

        # Then go over each verse.
        for verse in filedata[chapter].values():
            
            inter_text += verse + ". "

        ag_list.append(inter_text)
        ag_dict[chapter] = inter_text

    # If it is returned with flat = 1, as a list  of strings, then return this as-is.
    if flat == 1:
        print(f"I read in {filename}, with each list element containing a chapter as a string; this includes {len(ag_list)} list elements (and chapters).")
        return ag_dict
    
    # If flat = 2, then transform the values of ag_dict into a single string.
    if flat == 2:

        ret_str = ""

        for chapter in ag_list:
            ret_str += chapter + " "

        print(f"I read in {filename} as a single string; this includes {len(ret_str)} characters.")
        return ret_str

# This function defines the key phrase extraction methods. 
class kpe_class:
    def __init__(self):
                
        # Load in the API endpoint with keys from the JSON file. 
        path = "confidential\\"
        file = "keys.json"

        try:
            f = open(path + file, encoding='utf-8')
            keys_file = json.load(f)
            f.close()
            print(f"Keys file loaded.")
        except Exception as e:
            print(f"Error loading keys file: {e}. Please check path and file name.")

        try:
            # Define the keys and endpoint. 
            key = keys_file['key1']
            endpoint = keys_file['endpoint']
            print("Keys and endpoint found and defined.")
        except Exception as e:
            print(f"Error defining keys and endpoint: {e}. Please check keys file.")    

        #  Authenticate the client using your key and endpoint
        ta_credential = AzureKeyCredential(key)
        text_analytics_client = TextAnalyticsClient(
                endpoint=endpoint, 
                credential=ta_credential)

        try:
            self.client = text_analytics_client
            print("Client authenticated.")
        except:
            print(f"Could not authenticate client: {e}. ")

    # This code is based on the MS Azure Walkthrough: 
    # https://learn.microsoft.com/en-us/azure/ai-services/language-service/key-phrase-extraction/quickstart?pivots=programming-language-python

    # This function receives as arguments: 
    # text: strings of text to be analyzed.
    # client: the client object created by the authenticate_client() function.
    # shows_stats: a boolean value that determines whether or not to show statistics about the document payload.

    # It returns an ExtractKeyPhrases object, documented at this webpage: https://learn.microsoft.com/en-us/python/api/azure-ai-textanalytics/azure.ai.textanalytics.extractkeyphrasesresult?view=azure-python
    # It has the following attributes:
    # id:Unique, non-empty document identifier that matches the document id that was passed in with the request. If not specified in the request, an id is assigned for the document.
    # is_error: True or False. Boolean check for error item when iterating over list of results. Always False for an instance of a ExtractKeyPhrasesResult.
    # statistics: If show_stats=True was specified in the request this field will contain information about the document payload.
    def key_phrase_extraction(self,text,show_stats=True):
        
        print(f"Extracting key phrases from {text}...")
        try:
            
            # This method is documented here: https://learn.microsoft.com/en-us/python/api/azure-ai-textanalytics/azure.ai.textanalytics.textanalyticsclient?view=azure-python#azure-ai-textanalytics-textanalyticsclient-extract-key-phrases
            response_whole = self.client.extract_key_phrases(documents = text ,show_stats=show_stats)
            response=response_whole[0]

            if not response.is_error:
                print("\tKey Phrases:")
                for phrase in response.key_phrases:
                    print("\t\t", phrase)
                return response_whole
            else:
                print(response.id, response.error)

        except Exception as err:
            print("Encountered exception. {}".format(err))
            





