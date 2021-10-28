from django.urls import reverse
from django.db.models import Max
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import  render




from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


from .models import User, Category, AuctionListing, Bid, Comment,UserDetails



def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10



def index(request):
    objt = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "objects": objt
    })


def all(request):
    obj = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "objects": obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        #print(username,password)
        user = authenticate(request, username=username, password=password)


        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session['user_id']=user.id
            #print(request.session['user_id'])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    
    if request.method == "GET":
        return render(request, "auctions/login.html")


@login_required
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
            request.session['user_id']=user.id
            print(request.session['user_id'])
            print(" register")
            
        except IntegrityError as er:
            print(er)
            return render(request, "auctions/register.html", {
                "message": "Username or Email already taken."
            })
        login(request, user)
        return render(request, "auctions/userdetails.html")
    else:
        return render(request, "auctions/register.html")


@login_required
def UserDetailsView(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        card=request.POST["card"]
        userid=request.session.get("user_id")
        
        print(card,phone,userid)
        try:
            if not luhn_checksum(card):
                user = UserDetails.objects.create(userid=userid,phone=phone,card_number=card)
                user.save()
            else:
                 return render(request, "auctions/userdetails.html", {
                "message": "Card Invalid."
            }) 
            
        except IntegrityError as er:
            print(er)
            return render(request, "auctions/userdetails.html", {
                "message": "Username or Phone already taken."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/index.html")

@login_required
def createListing(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        startBid = request.POST["startBid"]
        category = Category.objects.get(id=request.POST["category"])
        user = request.user
        image = request.FILES["image"]
        image2 = request.FILES["image2"]
        vrmodel = request.FILES["vrmodel"]
        print(image.name,vrmodel.name)
        if  image:
            print(image)
            listing = AuctionListing.objects.create(
                name=title, category=category, date=timezone.now(), startBid=startBid, description=description, user=user,image=image,image2=image2,vrmodel=vrmodel, active=True)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("createListing"))
    return render(request, "auctions/createListing.html", {
        'categories': Category.objects.all()
    })


def details(request, id):
    item = AuctionListing.objects.get(id=id)
    bids = Bid.objects.filter(auctionListing=item)
    comments = Comment.objects.filter(auctionListing=item)
    value = bids.aggregate(Max('bidValue'))['bidValue__max']
    bid = None
    if value is not None:
        bid = Bid.objects.filter(bidValue=value)[0]
    return render(request, "auctions/details.html", {
        'item': item,
        'bids': bids,
        'comments': comments,
        'bid': bid
    })





    

def categories(request):
    if request.method == 'POST':
        category = request.POST["category"]
        new_category, created = Category.objects.get_or_create(
            name=category.lower())
        if created:
            new_category.save()
        else:
            messages.warning(request, "Category already Exists!")
        return HttpResponseRedirect(reverse("categories"))
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })


def filter(request, name):
    category = Category.objects.get(name=name)
    obj = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "objects": obj
    })


@login_required
def comment(request, id):
    if request.method == 'POST':
        auctionListing = AuctionListing.objects.get(id=id)
        user = request.user
        commentValue = request.POST["content"].strip()
        if(commentValue != ""):
            comment = Comment.objects.create(date=timezone.now(
            ), user=user, auctionListing=auctionListing, commentValue=commentValue)
            comment.save()
        return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def bid(request, id):
    if request.method == 'POST':
        auctionListing = AuctionListing.objects.get(id=id)
        bidValue = request.POST["bid"]
        args = Bid.objects.filter(auctionListing=auctionListing)
        value = args.aggregate(Max('bidValue'))['bidValue__max']
        if value is None:
            value = 0
        if float(bidValue) < auctionListing.startBid or float(bidValue) <= value:
            messages.warning(
                request, f'Bid Higher than: {max(value, auctionListing.startBid)}!')
            return HttpResponseRedirect(reverse("details", kwargs={'id': id}))
        user = request.user
        bid = Bid.objects.create(
            date=timezone.now(), user=user, bidValue=bidValue, auctionListing=auctionListing)
        bid.save()
    return HttpResponseRedirect(reverse("details", kwargs={'id': id}))


@login_required
def end(request, itemId):
    auctionListing = AuctionListing.objects.get(id=itemId)
    user = request.user
    if auctionListing.user == user:
        auctionListing.active = False
        auctionListing.save()
        messages.success(
            request, f'Auction for {auctionListing.name} successfully closed!')
    else:
        messages.info(
            request, 'You are not authorized to end this listing!')
    return HttpResponseRedirect(reverse("details", kwargs={'id': itemId}))


@login_required
def watchlist(request):
    if request.method == 'POST':
        user = request.user
        auctionListing = AuctionListing.objects.get(id=request.POST["item"])
        if request.POST["status"] == '1':
            user.watchlist.add(auctionListing)
        else:
            user.watchlist.remove(auctionListing)
        user.save()
        return HttpResponseRedirect(
            reverse("details", kwargs={'id': auctionListing.id}))
    return HttpResponseRedirect(reverse("index"))


@login_required
def watch(request):
    user = request.user
    obj = user.watchlist.all()
    return render(request, "auctions/index.html", {
        "objects": obj
    })


