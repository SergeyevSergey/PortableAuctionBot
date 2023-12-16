from django.contrib import admin
from .models import Lot, CustomUser, UserBid

# Register your models here.

admin.site.register(Lot)
admin.site.register(CustomUser)
admin.site.register(UserBid)
