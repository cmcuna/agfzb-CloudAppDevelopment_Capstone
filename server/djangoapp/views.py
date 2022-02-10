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
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

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
    else:
        return render(request, 'djangoapp/index.html', {
            #context
            "carmakelist": carmakelist
        })
        #return render(request, 'djangoapp/registration.html')
        

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

