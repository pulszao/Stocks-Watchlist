from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.core.paginator import Paginator
import requests


from .models import User, Transactions, Watchlist

# sass --watch styles.scss:styles.css
# Create your views here.
stocks_api_key = "pk_6e745d9628ba4988b0c47b5bd151622e"
news_api_key = "9e84e53491404cf3a278c553a3d40ab6"

@login_required(login_url='/login')
def index(request):

    stocks = "AAPL,FB,TSLA,AMZN,MSFT,ADBE,SPOT,BJ,DIS,CSCO" #get stocks
    types = "quote" #quote / chart
    stocks_url = "https://cloud.iexapis.com/stable/stock/market/batch"
    stocks_querystring = {"symbols": stocks,"types":types, "token": stocks_api_key}
    stocks_response = requests.request("GET", stocks_url, params=stocks_querystring).json

    news_url = 'https://newsapi.org/v2/top-headlines?'
    news_querystring = {"country": 'us',"category": 'business', "apiKey": news_api_key, "pageSize": 12}
    news_response = requests.request("GET", news_url, params=news_querystring).json
    
    a = {'a', 'b'}

    return render(request, "stock_manager/index.html",{
        "stocks": stocks_response,
        'a': a,
        "news": news_response,
    })

    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "stock_manager/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "stock_manager/login.html")


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
            return render(request, "stock_manager/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "stock_manager/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "stock_manager/register.html",)


def watchlist(request):
    if request.method == 'GET':
        stocks = Watchlist.objects.filter(user=request.user)
        stocks_response = ''

        if stocks:
            stocks_string = ''

            for symbol in stocks:
                stocks_string += f'{symbol.listing_symbol},'

            type = "quote"
            stocks_url = "https://cloud.iexapis.com/stable/stock/market/batch"
            stocks_querystring = {"symbols": stocks_string,"types":type, "token": stocks_api_key}
            stocks_response = requests.request("GET", stocks_url, params=stocks_querystring).json

        return render(request, "stock_manager/watchlist.html", {
            "stocks": stocks_response,
            "have_stocks": stocks
        })

    else:
        # increase list of stocks
        stock = request.POST['stock']
        new_stock = Watchlist(
            user=request.user,
            listing_symbol=stock.upper()
        )
        new_stock.save()

        # render updated watchlist
        stocks = Watchlist.objects.filter(user=request.user)
        stocks_string = ''

        for symbol in stocks:
            stocks_string += f'{symbol.listing_symbol},'

        type = "quote"
        stocks_url = "https://cloud.iexapis.com/stable/stock/market/batch"
        stocks_querystring = {"symbols": stocks_string,"types":type, "token": stocks_api_key}
        stocks_response = requests.request("GET", stocks_url, params=stocks_querystring).json

        return render(request, "stock_manager/watchlist.html", {
            "stocks": stocks_response,
            "have_stocks": True
        })


def remove_watchlist(request, stock):
    # delete selected stock 
    r = Watchlist.objects.get(user=request.user, listing_symbol=stock)
    r.delete()

    stocks = Watchlist.objects.filter(user=request.user)
    stocks_string = ''

    for symbol in stocks:
        stocks_string += f'{symbol.listing_symbol},'

    type = "quote"
    stocks_url = "https://cloud.iexapis.com/stable/stock/market/batch"
    stocks_querystring = {"symbols": stocks_string,"types":type, "token": stocks_api_key}
    stocks_response = requests.request("GET", stocks_url, params=stocks_querystring).json

    return render(request, "stock_manager/watchlist.html", {
        "stocks": stocks_response,
        "have_stocks": stocks_string

    })


def portfolio(request):
    # get user's transactions
    transactions = Transactions.objects.filter(user=request.user).order_by("symbol").all()
    stocks = {}
    stocks_final = {}
    stocks_string = ''
    
    if transactions:
        for symbol in transactions:
            if symbol.symbol not in stocks_string:
                stocks_string += f'{symbol.symbol},'

        type = "quote"
        stocks_url = "https://cloud.iexapis.com/stable/stock/market/batch"
        stocks_querystring = {"symbols": stocks_string,"types":type, "token": stocks_api_key}
        stocks_response = requests.request("GET", stocks_url, params=stocks_querystring).json()
        
        for i in transactions:
            if i.symbol not in stocks and i.shares != 0:
                info = {}
                stocks[i.symbol] = info
                info['total'] = i.price * i.shares
                info['shares'] = i.shares
                info['avarage'] = info['total'] / info['shares']
                info['actual_price'] = stocks_response[i.symbol]['quote']['iexRealtimePrice']
                
            else:
                info['total'] += i.price * i.shares
                info['shares'] += i.shares
                if info['shares'] != 0:
                    info['avarage'] = info['total'] / info['shares']
        
        # removing stocks with 0 shares 
        for i in stocks:
            if stocks[i]['shares'] != 0:
                stocks_final[i] = stocks[i]

    return render(request, "stock_manager/portfolio.html",{
        "stocks": stocks_final
    })


def transactions(request):
    if request.method == 'GET':
        transactions = Transactions.objects.filter(user=request.user).order_by("-date").all()
        # pagination
        paginator = Paginator(transactions, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "stock_manager/transactions.html", {
            "transactions": page_obj,
        })

    else:
        # add transactions
        stock = request.POST['stock']
        quantity = request.POST['quantity']
        price = request.POST['price']
        operation = request.POST['operation']
        date = request.POST['date']
        
        if operation == 'sell':
            quantity = -(int(request.POST['quantity']))
        
        new_transaction = Transactions(
            user=request.user,
            operation = operation.capitalize(),
            symbol = stock.upper(),
            shares = quantity,
            price = price,
            date = date,
        )
        new_transaction.save()

        # render updated transacions
        transactions = Transactions.objects.filter(user=request.user).order_by("-date").all()
        # pagination
        paginator = Paginator(transactions, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "stock_manager/transactions.html", {
            "transactions": page_obj
        })


def remove_transactions(request, id):
    # delete selected transactions 
    r = Transactions.objects.get(user=request.user, id=id)
    r.delete()

    transactions = Transactions.objects.filter(user=request.user)

    return render(request, "stock_manager/transactions.html", {
        "transactions": transactions
    })


def chart(request):
    if request.method == 'POST':
        stock = request.POST['stock']

        return render(request, "stock_manager/chart.html", {
            "stock": stock
        })
    
    else:
        return render(request, "stock_manager/chart.html")