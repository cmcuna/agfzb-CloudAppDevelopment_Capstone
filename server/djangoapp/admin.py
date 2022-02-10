from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
### from .models import related models ###
#from .models import User #, Listing, Category, Comment, Watchlist
from .models import User, CarMake, CarModel

### Note: we must resister in admin to be able to access with our created admin django credentials (superuser), 
# to add initial data (and delete) 
# and to delete anything prior to adding additional functionality ###

# Register your models here.

#admin.site.register(User)
admin.site.register(User)
#admin.site.register(UserAdmin)
admin.site.register(CarMake)
admin.site.register(CarModel)

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
