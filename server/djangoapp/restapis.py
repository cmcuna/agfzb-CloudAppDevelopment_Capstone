# from lib2to3.pytree import _Results
# from xmlrpc.client import ResponseError
import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, KeywordsOptions, CategoriesOptions
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("Get from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters; http query
        response = requests.get(url, headers={'Content-Type': 'applicaiton/json'}, 
                                params=kwargs)
    except:
        # If any errors occur
        print("Newtork exception occured")
    status_code = response.status_code
    print("With status {}: ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in 'doc' object
            dealer_doc = dealer["doc"] 
            # Create a CarDealer object with values in 'doc' object (this is a local object? it is not being saved in sqlite, but data is rendered in http response...)
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], 
                                   short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results
            









# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_request_by_id(url, dealerID):
    #print(dealerID)
    #dealerID = dealerID
    print("Get from id {} ".format(url))
    print(f"Dealer id: {dealerID}")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'applicaiton/json'}, 
                                params={'id': dealerID})
    except:
        # If any errors occur
        print("Newtork exception occured, didnt get dealer by ID")
    status_code = response.status_code
    print("With status {}: ".format(status_code))
    json_data = json.loads(response.text) #convert string/text to python dictionary

    """output json read"""
    #print(json_data) #print json data into terminal

    """format json output for easier read"""
    #print(json.dumps(json_data,indent=2))

    """print doc count in json data"""
    #print(json_data['rows'])

    """loop and print id and dealer name in json data"""
    # for item in json_data['rows']:
    #     id = item['doc']['id']
    #     short_name = item['doc']['short_name']
    #     print(id, short_name)

    """loop through and find dealership by dealer ID"""
    for item in json_data['rows']:
        id = item['doc']['id']
        if id == dealerID:
            name = item['doc']['full_name']
            print(id, name)
            print(item)
            json_data = item #load single item into json_data for return

    return json_data

def get_dealer_by_id(url, dealerID):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request_by_id(url, dealerID)
    if json_result:
        dealer_doc = json_result['doc'] 
        # Create a CarDealer object with values in 'doc' object (this is a local object? it is not being saved in sqlite, but data is rendered in http response...)
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], 
                                   short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
        results.append(dealer_obj)
    return results












# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    #ibm watson NLU url and api key
    apikey = 'zNRmRrgNzy6xKqYzZsvn_oJmNK6jLBFWYNRIwLkPlqOo'
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e31d5683-c594-434c-9b90-a97f537ac9a9'

    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(sentiment=SentimentOptions())).get_result()
        #features=Features(sentiment=SentimentOptions(targets=['bonds']))).get_result()
        #features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()

    print(json.dumps(response, indent=2))

    """extract sentiment"""
    sentiment = response['sentiment']['document']['label']
    print(f"Sentiment: {sentiment}")
    
    return sentiment

def get_request_review_id(url, dealerID):
    #print(dealerID)
    #dealerID = dealerID
    print("Get review from id {} ".format(url))
    print(f"Dealer id for review: {dealerID}")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'applicaiton/json'}, 
                                params={'id': dealerID}, 
                                auth=HTTPBasicAuth('apikey', 'zNRmRrgNzy6xKqYzZsvn_oJmNK6jLBFWYNRIwLkPlqOo'))
        #print("Pass Response...")
    except:
        # If any errors occur
        print("Newtork exception occured, didnt get dealer by ID")

    status_code = response.status_code
    print("With status {}: ".format(status_code))
    json_data = json.loads(response.text) #convert string/text to python dictionary

    """output json read"""
    print(json_data) #print json data into terminal

    """format json output for easier read"""
    #print(json.dumps(json_data,indent=2))

    """loop through and find dealership by dealer ID"""
    for item in json_data['rows']:
        id = item['doc']['id']
        if id == dealerID:
            short_name = item['doc']['name']
            review = item['doc']['review']
            #print(id, short_name, review)
            print(f"Dealer id: {id}, Dealer Name: {short_name}, Review: {review}")
            print(item)
            json_data = item #load single item into json_data for return

    return json_data

def get_dealer_reviews_from_cf(url, dealerID):
    results = []
    # Call get_request with a URL parameter (i.e. get review)
    json_result = get_request_review_id(url, dealerID)
    print(f"Review to be sent: {json_result['doc']['review']}")
    dealerreview = json_result['doc']['review']
    return_sentiment = analyze_review_sentiments(dealerreview)
    #print(f"Return Sentiment:{return_sentiment}")
    if json_result:
        dealer_doc = json_result['doc'] 
        # Create a CarDealer object with values in 'doc' object (this is a local object? it is not being saved in sqlite, but data is rendered in http response...)
        dealer_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"], 
                                car_model=dealer_doc["car_model"], car_year=dealer_doc["car_year"], id=dealer_doc["id"],
                                sentiment=return_sentiment)
        results.append(dealer_obj)

    return results
