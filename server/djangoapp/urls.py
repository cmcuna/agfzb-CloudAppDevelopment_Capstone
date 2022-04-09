from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for index route
    path(route='', view=views.get_dealerships, name='index'),

    # path for about view
    path(route='about', view=views.about, name='about'),
    
    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for registration
    path(route='registration', view=views.registration, name='registration'),

    # path for login
    path(route='login', view=views.login, name='login'),
    
    # path for financing
    path(route='financing', view=views.financing, name='financing'),
    
    # path for dealer data (testing data return, should be deleted later...)
    path(route='dealerdata', view=views.get_cloudDealers, name='dealerdata'),

    # path for dealer data (testing data return, should be deleted later...)
    path(route='dealerdataID', view=views.get_cloudDealerbyID, name='dealerdataID'),

    # path for dealer data (testing data return, should be deleted later...)
    path(route='dealerReviewID', view=views.get_dealer_reviews, name='dealerdetails'),

    # path for logout  

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)