from django.contrib import admin
from .models import Category, AuctionListing, User, Comment, Bid, UserDetails

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


admin.site.register(User, UserAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'phone', ]


admin.site.register(UserDetails, UserDetailsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Category, CategoryAdmin)


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'startBid', 'user_id', 'active']


admin.site.register(AuctionListing, AuctionListingAdmin)


admin.site.register(Bid)
admin.site.register(Comment)
