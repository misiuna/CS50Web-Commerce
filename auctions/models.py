from django.contrib.auth.models import AbstractUser
from django.db import models


# allow users to post auction listings, 
# place bids on listings, 
# comment on those listings, 
# and add listings to a “watchlist.”

# 4 models: User, auction listings, bids, comments made on auction listings. 

class User(AbstractUser):
    userWatchlist = models.ManyToManyField('Listing', related_name='userWatchlist', blank=True)
    pass
    def __str__(self):
        return f"{self.username}"
    #name that appears as an object in Users

class Listing(models.Model):
    image = models.URLField(max_length=600, default="")
    title = models.CharField(max_length = 45)
    description = models.CharField(max_length = 520)
    price = models.IntegerField()
    category = models.CharField(max_length=32, default="")
    status = models.CharField(max_length=32, default="")
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAllListings", default = "")

    def __str__(self):
        return f"{self.title}"
    
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = "")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default="", related_name="allListingBids")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.listing} : {self.bid}"

class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="allListingComments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAllComments")
    comment = models.CharField(max_length=520)

    def __str__(self):
        return f"{self.comment} \n - {self.user}"
