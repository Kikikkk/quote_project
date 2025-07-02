from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404

from quotes.models import Quote, Vote
from .forms import QuoteForm
from .utils import get_random_quote
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'quotes/register.html', {'form': form})

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

@login_required
def like_quote(request, quote_id):
    return handle_vote(request, quote_id, 'like')

@login_required
def dislike_quote(request, quote_id):
    return handle_vote(request, quote_id, 'dislike')

def handle_vote(request, quote_id, vote_type):
    quote = Quote.objects.get(id=quote_id)
    user = request.user

    existing_vote = Vote.objects.filter(user=user, quote=quote).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})
        else:
            if existing_vote.vote_type == 'like':
                quote.likes -= 1
                quote.dislikes += 1
            else:
                quote.dislikes -= 1
                quote.likes += 1
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        Vote.objects.create(user=user, quote=quote, vote_type=vote_type)
        if vote_type == 'like':
            quote.likes += 1
        else:
            quote.dislikes += 1

    quote.save()
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})

def top_quotes(request):
    sort = request.GET.get('sort', 'likes')
    if sort not in ['likes', 'dislikes', 'views']:
        sort = 'likes'
    quotes = Quote.objects.order_by(f'-{sort}')[:10]
    return render(request, 'quotes/top_quotes.html', {'quotes': quotes, 'sort': sort})
