
# Here is the MS documentation for this libary: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme?view=azure-python
# And even more detailed here: https://learn.microsoft.com/en-us/python/api/azure-ai-textanalytics/azure.ai.textanalytics?view=azure-python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import json


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
            





