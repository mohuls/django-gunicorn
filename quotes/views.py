from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForms
from django.contrib import messages

def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_d7f023faec384ea598edc4f584ca77a9")

        try:
            api = json.loads(api_request.content)
        except Exception:
            api = "Error..."
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': "Enter a company name to get quote"})

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    if request.method == 'POST':
        form = StockForms(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added!"))
            return redirect('add_stock')
        else:
            messages.warning(request, ("Please enter a valid stock"))
    else:
        import requests
        import json
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_d7f023faec384ea598edc4f584ca77a9")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception:
                api = "Error..."

        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output })

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Item has been deleted!"))
    return redirect(delete_stock)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})
