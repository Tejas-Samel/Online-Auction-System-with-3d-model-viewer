from django.contrib.auth.models import AbstractUser
from django.db import models





class User(AbstractUser):
    watchlist = models.ManyToManyField(
        'AuctionListing', blank=True, related_name="userWatchlist")

class UserDetails(models.Model):
    userid=models.CharField(max_length=10,default=None)
    card_number = models.CharField(max_length=20,default=0)
    phone = models.CharField(max_length=15,default=0)




class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.id} : {self.name}"


class AuctionListing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    startBid = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="products/",null=True)
    image2 = models.FileField(upload_to="products/",null=True)
    vrmodel = models.FileField(upload_to="products/",null=True)
    active = models.BooleanField()

    def __str__(self):
        return f"{self.id} : {self.name} in {self.category.name}\nPosted at : {self.date}\nValue : {self.startBid}\nDescription : {self.description}\nPosted By : {self.user.username} Active Status: {self.active}"


class Bid(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bidValue = models.DecimalField(decimal_places=2, max_digits=7)
    auctionListing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} : {self.user.username} bid {self.bidValue} on {self.auctionListing.name} at {self.date}"


class Comment(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auctionListing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE)
    commentValue = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.id} : {self.user.username} commented on {self.auctionListing.name} posted by {self.auctionListing.user.username} at {self.date} : {self.commentValue}"
