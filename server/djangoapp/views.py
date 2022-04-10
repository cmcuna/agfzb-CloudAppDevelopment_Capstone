from unittest import loader
from urllib import response
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
#from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import User, CarMake, CarModel
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import IntegrityError
from django.template.loader import get_template
from datetime import datetime
import logging, json
from .restapis import get_dealers_from_cf, get_request
from .restapis import get_dealer_by_id, get_request_by_id
from .restapis import get_dealer_reviews_from_cf, get_request_review_id
from .restapis import post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

def get_cloudDealers(request):
    context = {}
    if request.method == "GET":
        url ='https://9a1758aa.us-south.apigw.appdomain.cloud/api/dealership'
        # Get dealers from the URL
        print("Get from {} ".format(url)) #this string will print out in VScode (IDE)
        # Call get method of requests library with URL and parameters
        dealerships = get_dealers_from_cf(url)
        context = dealerships
        # concat all dealer's short name
        #dealer_names = ', '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)#, content_type='application/json')

        # Return dealers with render (in lieu of HttpResponse), HttpResponse better for data dumps without templates being rendered
        return render(request, 'djangoapp/getdealerdata.html', {
            'dealerdata': context
        })
        
def get_cloudDealerbyID(request):
    if request.method == "GET":
        url ='https://9a1758aa.us-south.apigw.appdomain.cloud/api/dealership'
        # Get dealers from the URL
        print("Get from {} ".format(url))
        # Call get method of requests library with URL and parameters
        dealerID = 1
        dealerships = get_dealer_by_id(url, dealerID)
        # concat all dealer's short name
        dealer_name_by_id = ', '.join([dealer.full_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)#, content_type='application/json')

        # Return dealers with render (in lieu of HttpResponse), HttpResponse better for data dumps without templates being rendered
        return render(request, 'djangoapp/getdealerdatabyID.html', {
            'dealerdata': dealer_name_by_id
        })

def get_dealer_reviews(request):
    
    if request.method == "GET":
        #url ='https://9a1758aa.us-south.apigw.appdomain.cloud/reviews/reviews'
        url ='https://9a1758aa.us-south.apigw.appdomain.cloud/reviews/reviews'
        # Get dealers from the URL
        print("Get from {} ".format(url))
        # Call get method of requests library with URL and parameters
        dealerID = 2
        dealerships = get_dealer_reviews_from_cf(url, dealerID)
        # concat all dealer's short name
        #dealer_review_by_id = ', '.join([dealer.name for dealer in dealerships])
        for dealer in dealerships:
            #create list for next iteration, maybe have multi reviews for single dealer?
            review = dealer.review
            sentiment = dealer.sentiment
        #dealer_review_by_id = sentiment
        dealer_review_by_id = "Review: '" + review + "'" + "\nSentiment of review: " + sentiment
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)#, content_type='application/json')

        # Return dealers with render (in lieu of HttpResponse), HttpResponse better for data dumps without templates being rendered
        return render(request, 'djangoapp/getdealerreview.html', {
            'dealerdata': dealer_review_by_id
        })
        
# Create an 'add_review' django view to post a dealer review: verify user auth for post and create dict object for reviews to append
def add_review(request):
    #create a reviews dictionary for appending and add attributes defined in reviews object
    review = {}
    review["id"]=51
    review["name"]="John Bass Doe"
    review["dealership"]=15
    review["review"]="Great service, great vehicle, great experience."
    review["purchase"]=True
    review["purchase_date"]="04/09/2022"
    review["car_make"]="Toyota"
    review["car_model"]="4Runner"
    review["car_year"]=2021
    #review["time"]=datetime.utcnow().isoformat() #time of review POST
    #create a payload dictionary and assign one key called review. 'review' will be the appended dictionary variable above
    json_payload = {}
    json_payload["review"] = review

    print("Json Payload:", json_payload)
    
    dealerID = review["id"]
    print("Post Dealer ID: ", dealerID)
    
    if request.method=="GET": #this should be POST
        #Same API for GET/POST. Both are within the 'Review' APIs
        url ='https://9a1758aa.us-south.apigw.appdomain.cloud/reviews/reviews'
        return_post = post_request(url, review)
        
        # Return dealers with render (in lieu of HttpResponse), HttpResponse better for data dumps without templates being rendered
        return render(request, 'djangoapp/postdealerreview.html', {
            'dealerdata': return_post
        })

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    carmakelist = CarMake.objects.all() #variable unused
    carmodellist = CarModel.objects.all() #variable unused
    context = {}
    if request.method == "POST":
        carmakename = request.POST["carmakename"]
        carmakedescription = request.POST["carmakedescription"]

        #attemtp to create new entry for car make and car description
        try:
            newcarmake = CarMake.objects.create(carMakeName=carmakename, carDescription=carmakedescription)
            newcarmake.save()
        except IntegrityError:
            return render(request, "djangoapp/registration.html", {
                "message": "Error creating car make entry."
            })
        return HttpResponseRedirect(reverse("index"))
    else: #this is GET request
        return render(request, 'djangoapp/index.html', {
            #context    
            "carmakelist": carmakelist
        })
        
        

# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')
    
# Create a `financing` view to return a static page
def financing(request):
    if request.method == "GET":
        return render(request, 'djangoapp/financing.html')

# Create a `sign in` view
def login(request):
    if request.method == "GET":
        return render(request, 'djangoapp/login.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
def registration(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        #ensure password matches confirmation password
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "djangoapp/registration.html", {
                "message": "Passwords must match. Please re-enter."
            })
        
        #attemtp to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "djangoapp/registration.html", {
                "message": "Username already take."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'djangoapp/registration.html')
    

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

