from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required
from .choices import *

from .models import User, Listing, Comments, Bids
from django import forms

# allow users to post auction listings, 
# place bids on listings, 
# comment on those listings, 
# and add listings to a “watchlist.”

class NewListingForm(forms.Form):
    image = forms.URLField(max_length=600)
    
    title = forms.CharField(label="title")
    description = forms.CharField(label="description")
    price = forms.IntegerField()
    category = forms.ChoiceField(choices=Category_CHOICES)
    status = forms.ChoiceField(choices=Status_CHOICES)

class NewCommentForm(forms.Form):
    comment = forms.CharField(label="comment", max_length=520)

class NewBidForm(forms.Form):
    bid = forms.IntegerField()

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "activeListings": Listing.objects.filter(status="Active"),
        "closedListings": Listing.objects.filter(status="Closed")
    })

@login_required
def createListing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            status = form.cleaned_data["status"]
            date = datetime.datetime.now()
            user = request.user
            listing = Listing.objects.create(image=image, title=title, description=description, status=status, price=price, category=category, date=date, user=user)
            listing.save()
            
            return HttpResponseRedirect('/', {
                "listings": Listing.objects.all()
            })   
    return render(request, "auctions/createListing.html", {
        "form": NewListingForm()
    })

@login_required
def listing(request, id):
    thisListing = Listing.objects.get(pk=id)
    thisListingBids = Bids.objects.filter(listing=thisListing.id)
    if thisListingBids:
        finalBidder = thisListingBids.last().user
    else:
        finalBidder = "none"
    user = request.user
    if not thisListingBids:
        thisListingLastBid = 0
    else:
        thisListingLastBid = thisListingBids.last().bid
    currentPrice = thisListing.price
    username = user.username
    fullWatchlist = user.userWatchlist.all()
    noWatchlist = (thisListing in list(fullWatchlist))
    if request.method == "POST":
        form = NewBidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            if bid <= currentPrice or bid <= thisListingLastBid:
                return render(request, "auctions/listing.html", {
                    "message": (f"Your bid must be greater than ${currentPrice}. Try again!"),
                    "form": NewBidForm(),
                    "id": id,
                    "listings": thisListing,
                    "fullWatchlist": fullWatchlist,
                    "noWatchlist": noWatchlist,
                    "comments": Comments.objects.all()
                })
            #take new bid and replace current price value with it
            thisListing.price = bid
            thisListing.save()
            newBid = Bids(user=user, listing=thisListing, bid = bid)
            newBid.save()
            return render(request, "auctions/listing.html", {
                "message": (f"Your bid of ${bid} was sucessfull."),
                "form": NewBidForm(),
                "id": id,
                "listings": thisListing,
                "fullWatchlist": fullWatchlist,
                "noWatchlist": noWatchlist,
                "comments": Comments.objects.filter(listing=thisListing.id)
            })
    return render(request, "auctions/listing.html", {
        "form": NewBidForm(),
        "user": user,
        "id": id,
        "listings": thisListing,
        "fullWatchlist": fullWatchlist,
        "noWatchlist": noWatchlist,
        "finalBidder": finalBidder,
        "comments": Comments.objects.filter(listing=thisListing.id)
        })

def closeBid(request, id):
    user=request.user
    thisListing = Listing.objects.get(pk=id)
    thisListing.status = "Closed"
    thisListing.save()
    return render(request, "auctions/listing.html", {
        "form": NewBidForm(),
        "id": id,
        "listings": thisListing,
        "closeBid": (f"Your listing is now closed."),
        "comments": Comments.objects.filter(listing=thisListing.id)
    })    

def categories(request):
    categories = Category_CHOICES
    if request.method == "GET":
        for x, y in categories:
            requestCategory = request.GET.get(x)
            if requestCategory == x:
                activeListings = Listing.objects.filter(category=x, status="Active")
                closedListings = Listing.objects.filter(category=x, status="Closed")
                return render(request, "auctions/index.html", {
                    "listings": Listing.objects.filter(category=x),
                    "activeListings": activeListings,
                    "closedListings": closedListings,
                    "activeListingsCount": activeListings.count(),
                    "closedListingsCount": closedListings.count(),
                    "title": x    
                })
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required
def watchlist(request):
    user = request.user
    watchlist = user.userWatchlist.all()
    return render(request, "auctions/watchlist.html",{
        "watchlist": watchlist
    })

@login_required
def addTOwatchlist(request, id):
    thisListing = Listing.objects.get(pk=id)
    listingID = Listing.objects.get(pk=id).id
    user = request.user
    allwatchlist = user.userWatchlist.all()
    hasListing = user.userWatchlist.filter(pk = listingID).count()
    
    #if listing already exists - remove from watchlist
    if hasListing > 0:
        user.userWatchlist.remove(id)
        return HttpResponseRedirect(reverse("listing", args=str(listingID)), {
            "listings": thisListing,
            "user": user,
            "watchlist": allwatchlist,
            "hasListing": hasListing,
        })
    #if listing does not exist - add to watchlist
    else:
        user.userWatchlist.add(id)

        return HttpResponseRedirect(reverse("listing", args=str(listingID)), {
            "listings": thisListing,
            "user": user,
            "watchlist": allwatchlist,
            "hasListing": hasListing
        })

@login_required
def comment(request, id):
    thisListing = Listing.objects.get(pk=id)
    thisListingComments = Comments.objects.filter(listing=thisListing.id) 
    listingID = thisListing.id
    user = request.user
    if request.method == "POST":
        commentForm = NewCommentForm(request.POST)
        date = datetime.datetime.now()
        if commentForm.is_valid():
            comment = commentForm.cleaned_data["comment"]
            newComment = Comments(listing=thisListing, user=user, comment=comment)
            newComment.save()
            return HttpResponseRedirect(reverse("listing", args=str(listingID)), {
                "listings": thisListing,
                "user": thisListingComments.values('user'),
                "commentForm": NewCommentForm(),
                "comments": thisListingComments
            })    
    return HttpResponseRedirect(reverse("listing", args=str(listingID)), {
        "listings": thisListing,
        "user": thisListingComments.values('user'),
        "commentForm": NewCommentForm(),
        "comments": thisListingComments
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
