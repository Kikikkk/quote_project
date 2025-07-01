from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404

from quotes.models import Quote
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

def like_quote(request, quote_id):
    if request.method == 'POST':
        try:
            quote = Quote.objects.get(id=quote_id)
            quote.likes += 1
            quote.save()
            return JsonResponse({'likes': quote.likes})
        except Quote.DoesNotExist:
            raise Http404
    return JsonResponse({'error': 'Invalid method'}, status=405)

def dislike_quote(request, quote_id):
    if request.method == 'POST':
        try:
            quote = Quote.objects.get(id=quote_id)
            quote.dislikes += 1
            quote.save()
            return JsonResponse({'dislikes': quote.dislikes})
        except Quote.DoesNotExist:
            raise Http404
    return JsonResponse({'error': 'Invalid method'}, status=405)

def top_quotes(request):
    quotes = Quote.objects.order_by('-likes')[:10]
    return render(request, 'quotes/top_quotes.html', {'quotes': quotes})

