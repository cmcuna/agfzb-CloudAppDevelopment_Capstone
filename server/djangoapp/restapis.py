# from lib2to3.pytree import _Results
# from xmlrpc.client import ResponseError
import requests
import json
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












# # Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# # def analyze_review_sentiments(text):
# # - Call get_request() with specified arguments
# # - Get the returned sentiment label such as Positive or Negative

# def get_request_review_id(url, dealerID):
#     #print(dealerID)
#     #dealerID = dealerID
#     print("Get from id {} ".format(url))
#     print(f"Dealer id: {dealerID}")
#     try:
#         # Call get method of requests library with URL and parameters
#         response = requests.get(url, headers={'Content-Type': 'applicaiton/json'}, 
#                                 params={'id': dealerID})
#     except:
#         # If any errors occur
#         print("Newtork exception occured, didnt get dealer by ID")
#     status_code = response.status_code
#     print("With status {}: ".format(status_code))
#     json_data = json.loads(response.text) #convert string/text to python dictionary

#     """output json read"""
#     #print(json_data) #print json data into terminal

#     """format json output for easier read"""
#     #print(json.dumps(json_data,indent=2))

#     """print doc count in json data"""
#     #print(json_data['rows'])

#     """loop and print id and dealer name in json data"""
#     # for item in json_data['rows']:
#     #     id = item['doc']['id']
#     #     short_name = item['doc']['short_name']
#     #     print(id, short_name)

#     """loop through and find dealership by dealer ID"""
#     for item in json_data['rows']:
#         id = item['doc']['id']
#         if id == dealerID:
#             short_name = item['doc']['short_name']
#             print(id, short_name)
#             print(item)
#             json_data = item #load single item into json_data for return

#     return json_data

# def get_dealer_reviews_from_cf(url, dealerID):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request_review_id(url, dealerID)
#     if json_result:
#         dealer_doc = json_result['doc'] 
#         # Create a CarDealer object with values in 'doc' object (this is a local object? it is not being saved in sqlite, but data is rendered in http response...)
#         dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
#                                 id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], 
#                                 short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
#         results.append(dealer_obj)
#     return results
