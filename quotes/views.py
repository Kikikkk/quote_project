from django.shortcuts import render, redirect
from .forms import QuoteForm
from .utils import get_random_quote

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def home(request):
    quote = get_random_quote()
    if quote:
        quote.views += 1
        quote.save()
    return render(request, 'quotes/home.html', {'quote': quote})
